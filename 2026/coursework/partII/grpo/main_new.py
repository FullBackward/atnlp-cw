import re
import os
import argparse
import random
import numpy as np
import torch
import wandb

from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, PeftModel
from trl import GRPOTrainer, GRPOConfig

from dataset import build_rl_dataset


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def _completion_to_text(c):
    if c is None:
        return ""
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        return c.get("content") or c.get("generated_text") or c.get("text") or str(c)
    if isinstance(c, (list, tuple)):
        if len(c) > 0 and isinstance(c[0], dict) and "content" in c[0]:
            return "\n".join(m.get("content", "") for m in c if isinstance(m, dict))
        if len(c) > 0 and isinstance(c[0], (list, tuple)):
            return "\n".join(_completion_to_text(x) for x in c)
        return "\n".join(_completion_to_text(x) for x in c)
    return str(c)


def _parse_number(s: str):
    s = s.replace(",", "").strip()
    try:
        return int(s) if re.fullmatch(r"[-+]?\d+", s) else float(s)
    except ValueError:
        return None


def _extract_gt(answer):
    nums = re.findall(r"[-+]?\d[\d,]*\.?\d*", str(answer))
    if not nums:
        return None
    return _parse_number(nums[-1])


def _count_phrase(text: str) -> int:
    return len(re.findall(r"(?i)\bthe answer is\b", text))


def _final_nonempty_line(text: str):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _has_bad_answer_format(text: str) -> bool:
    """
    Reject bad answer forms such as:
      The answer is [40]
      The answer is \\boxed{40}
      The answer is \\[\\boxed{40}\\]
      The answer is: the answer is 40
    """
    text = text.strip()

    bad_patterns = [
        r"(?i)\bthe answer is\b[:\s]*\[\s*[-+]?\d[\d,]*\.?\d*\s*\]",                 # [40]
        r"(?i)\bthe answer is\b[:\s]*\\+boxed\{\s*[-+]?\d[\d,]*\.?\d*\s*\}",         # \boxed{40}
        r"(?i)\bthe answer is\b[:\s]*\\+\[\s*\\+boxed\{\s*[-+]?\d[\d,]*\.?\d*\s*\}\s*\\+\]",  # \[\boxed{40}\]
        r"(?i)\bthe answer is\b[:\s]*\bthe answer is\b",                             # repeated phrase
        r"(?i)\bthe answer is\b[:\s]*\\+\(\s*\\+boxed\{\s*[-+]?\d[\d,]*\.?\d*\s*\}\s*\\+\)"
    ]
    return any(re.search(p, text) for p in bad_patterns)


def _extract_pred_strict(text: str):
    """
    Strict format:
    - exactly one occurrence of 'the answer is'
    - no bad formats
    - final non-empty line is exactly:
        The answer is 40
      or
        The answer is: 40
    """
    text = text.strip()

    if _count_phrase(text) != 1:
        return None

    if _has_bad_answer_format(text):
        return None

    final_line = _final_nonempty_line(text)
    if not final_line:
        return None

    m = re.fullmatch(
        r"(?i)the answer is[:\s]*([-+]?\d[\d,]*\.?\d*)",
        final_line,
    )
    if not m:
        return None

    return _parse_number(m.group(1))


def _extract_pred_loose(text: str):
    """
    Semi-strict correctness extraction:
    1) prefer number after 'the answer is'
    2) otherwise fallback to last number anywhere
    """
    if not text:
        return None

    m = re.search(r"(?i)\bthe answer is\b[:\s]*([-+]?\d[\d,]*\.?\d*)", text)
    if m:
        return _parse_number(m.group(1))

    nums = re.findall(r"[-+]?\d[\d,]*\.?\d*", text)
    if not nums:
        return None
    return _parse_number(nums[-1])

def _strict(text):
    final_answer_match = re.search(r"The answer is[:\s]*([^\.\n]+)", text, re.IGNORECASE)

    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()
    else:
        fallback = re.findall(r"-?\d+\.?\d*", text)
        if fallback:
            final_answer = fallback[-1]
        else:
            final_answer = "Invalid"
    return final_answer

def format_reward_func(completions, **kwargs):
    """
    Fully strict format reward:
    +1.0 only if the output matches the exact clean final format.
     0.0 otherwise.
    """
    rewards = []
    for c in completions:
        text = _completion_to_text(c)
        final_answer = _strict(text)
        if final_answer == "Invalid":
            rewards.append(0.0)
        else:
            rewards.append(1.0)
    return rewards


def correctness_reward_func(prompts, completions, answer, **kwargs):
    """
    Semi-strict correctness:
    +2.0 if correct and strictly formatted
    +1.0 if correct but not strictly formatted
     0.0 otherwise
    """
    rewards = []
    answers = list(answer) if isinstance(answer, (list, tuple)) else [answer] * len(completions)

    for c, a in zip(completions, answers):
        text = _completion_to_text(c)
        gt = _extract_gt(a)

        if gt is None:
            rewards.append(0.0)
            continue

        valid = _strict(text)
        pred_strict = _extract_pred_strict(text)
        if valid != "invalid" and pred_strict == gt:
            rewards.append(3.0)
            continue

        pred_loose = _extract_pred_loose(text)
        if pred_loose is not None and pred_loose == gt:
            rewards.append(2.0)
        else:
            rewards.append(0.0)

    return rewards


def main():
    parser = argparse.ArgumentParser(description="GRPO Training Script")
    parser.add_argument("--model_signature", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_path", required=True, help="Path to the SFT adapter checkpoint")
    parser.add_argument("--output_path", required=True, help="Path to save the GRPO adapter")
    parser.add_argument("--wandb_project", default="nlu-gsm8k-grpo")
    parser.add_argument("--wandb_token", required=True)
    args = parser.parse_args()

    if args.wandb_token:
        wandb.login(key=args.wandb_token)

    os.environ["WANDB_PROJECT"] = args.wandb_project
    os.environ["WANDB_LOG_MODEL"] = "false"
    os.environ["WANDB_WATCH"] = "false"

    set_seed(42)

    run_name = os.path.basename(args.output_path.rstrip("/"))

    tokenizer = AutoTokenizer.from_pretrained(args.model_signature, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        args.model_signature,
        torch_dtype=torch.float16,
        attn_implementation="sdpa",
    )

    model = PeftModel.from_pretrained(base_model, args.adapter_path)
    model = model.merge_and_unload()

    grpo_peft_config = LoraConfig(
        task_type="CAUSAL_LM",
        r=8,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        target_modules=["q_proj", "k_proj"],
    )

    dataset = load_from_disk("dataset/gsm8k_500_grpo")
    train_dataset = dataset.map(build_rl_dataset)

    training_args = GRPOConfig(
        output_dir=args.output_path,
        run_name=run_name,
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_generations=4,
        max_prompt_length=256,
        max_completion_length=256,
        num_train_epochs=1,
        fp16=True,
        logging_steps=5,
        report_to="wandb",
        save_strategy="steps",
        save_steps=100,
        beta=0.1,
    )

    trainer = GRPOTrainer(
        model=model,
        reward_funcs=[correctness_reward_func, format_reward_func],
        args=training_args,
        train_dataset=train_dataset,
        processing_class=tokenizer,
        peft_config=grpo_peft_config,
    )

    trainer.train()
    trainer.save_model(args.output_path)
    wandb.finish()


if __name__ == "__main__":
    main()