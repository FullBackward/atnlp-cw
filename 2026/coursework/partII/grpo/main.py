import re
import torch
import random
import numpy as np
import os
import argparse
from datasets import load_from_disk
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, PeftModel, get_peft_model
from trl import GRPOTrainer, GRPOConfig
import wandb
from dataset import build_rl_dataset

def set_seed(seed=42):
    """Set seed for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    os.environ['PYTHONHASHSEED'] = str(seed)

def _completion_to_text(c):
    """
    TRL/GRPO completions can be:
      - a string
      - a dict like {"content": "..."} or {"generated_text": "..."}
      - a list of chat messages [{"role":..., "content":...}, ...]
      - a nested list like [[{"role":...,"content":...}]] depending on pipeline
    This normalizes to plain text.
    """
    if c is None:
        return ""
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        return c.get("content") or c.get("generated_text") or c.get("text") or str(c)
    if isinstance(c, (list, tuple)):
        # list of messages?
        if len(c) > 0 and isinstance(c[0], dict) and "content" in c[0]:
            return "\n".join(m.get("content", "") for m in c if isinstance(m, dict))
        # nested list?
        if len(c) > 0 and isinstance(c[0], (list, tuple)):
            return "\n".join(_completion_to_text(x) for x in c)
        return "\n".join(_completion_to_text(x) for x in c)
    return str(c)

def _extract_number(text: str):
    """
    Extract a numeric answer.
    Priority:
      1) number following 'the answer is'
      2) last number anywhere in the text
    Returns float or int when clean, else None.
    """
    if not text:
        return None

    # 1) Prefer "the answer is <number>"
    m = re.search(r"(?i)\bthe answer is\b\s*([-+]?\d[\d,]*\.?\d*)", text)
    if m:
        s = m.group(1).replace(",", "")
        try:
            return int(s) if re.fullmatch(r"[-+]?\d+", s) else float(s)
        except ValueError:
            pass

    # 2) Fallback: last number in the text
    nums = re.findall(r"[-+]?\d[\d,]*\.?\d*", text)
    if not nums:
        return None
    s = nums[-1].replace(",", "")
    try:
        return int(s) if re.fullmatch(r"[-+]?\d+", s) else float(s)
    except ValueError:
        return None

def _extract_gt_answer(ans):
    """
    Ground-truth may be:
      - '42'
      - '... #### 42'
      - list of such strings
    Returns float/int or None.
    """
    if ans is None:
        return None
    if isinstance(ans, (list, tuple)):
        # assume aligned with completions; extraction done per-item elsewhere
        return None
    ans_str = str(ans)
    return _extract_number(ans_str)

def _as_list(x, n):
    """Broadcast scalars to length n; keep lists as-is."""
    if isinstance(x, (list, tuple)):
        return list(x)
    return [x] * n


# ---------- reward functions ----------
def format_reward_func(completions, **kwargs):
    """
    Reward for adhering to the SFT format:
      - must contain the phrase "the answer is" (case-insensitive)
      - optionally, you can require a number right after it (enabled below)
    """
    rewards = []
    for c in completions:
        text = _completion_to_text(c)

        has_phrase = re.search(r"(?i)\bthe answer is\b", text) is not None

        # If you want to be stricter (phrase + number), use:
        has_phrase_and_number = re.search(
            r"(?i)\bthe answer is\b\s*([-+]?\d[\d,]*\.?\d*)", text
        ) is not None

        # Choose one:
        rewards.append(1.0 if has_phrase_and_number else 0.0)
        # rewards.append(1.0 if has_phrase else 0.0)

    return rewards


def correctness_reward_func(prompts, completions, answer, **kwargs):
    """
    Reward for getting the correct numeric answer.
    - Extract numeric prediction from completion (prefer after 'the answer is')
    - Extract numeric ground-truth from `answer`
    - Reward 1.0 if equal, else 0.0
    """
    rewards = []
    n = len(completions)

    answers = _as_list(answer, n)

    for c, a in zip(completions, answers):
        pred_text = _completion_to_text(c)
        pred_num = _extract_number(pred_text)

        gt_num = _extract_number(str(a))  # handles "#### 42" too

        if pred_num is None or gt_num is None:
            rewards.append(0.0)
            continue

        # Exact numeric match (int/float). If you want tolerance, change below.
        rewards.append(1.0 if pred_num == gt_num else 0.0)

    return rewards

def main():
    parser = argparse.ArgumentParser(description="GRPO Training Script")
    parser.add_argument("--model_signature", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--adapter_path", required=True, help="Path to the SFT adapter checkpoint")
    parser.add_argument("--output_path", required=True, default="./grpo_output")
    parser.add_argument("--wandb_project", default="nlu-gsm8k-grpo")
    parser.add_argument("--wandb_token", required=True, default=None)

    args = parser.parse_args()

    if args.wandb_token:
        print(f"Logging into WandB with provided token {args.wandb_token}...")
        wandb.login(key=args.wandb_token)

    RUN_NAME = args.output_path.split('/')[-1]

    # Setup WandB
    os.environ["WANDB_PROJECT"] = args.wandb_project
    os.environ["WANDB_LOG_MODEL"] = "false"
    os.environ["WANDB_WATCH"] = "false"
    
    set_seed(42)

    # 1. Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_signature, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 2. Load Base Model
    print(f"Loading Base Model: {args.model_signature}...")
    base_model = AutoModelForCausalLM.from_pretrained(
        args.model_signature,
        torch_dtype=torch.float16,
        device_map="auto",
        attn_implementation="sdpa"
    )

    # 3. Load and Merge SFT Adapter
    print(f"Loading and Merging SFT Adapter from {args.adapter_path}...")
    model = PeftModel.from_pretrained(base_model, args.adapter_path)
    model = model.merge_and_unload()
    
    # 4. Config for the NEW Adapter (RL Adapter)
    grpo_peft_config = LoraConfig(
        task_type="CAUSAL_LM",
        r=8,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        target_modules=["q_proj", "k_proj"],
    )

    # 5. Prepare Dataset
    dataset = load_from_disk("dataset/gsm8k_500_grpo")
    
    train_dataset = dataset.map(build_rl_dataset)

    training_args = GRPOConfig(
        output_dir=args.output_path,
        run_name=RUN_NAME,
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_generations=4,
        max_prompt_length=256,
        max_completion_length=256,
        num_train_epochs=1,
        bf16=True,
        logging_steps=5,
        report_to="wandb",
        save_strategy="steps",
        save_steps=100,
        beta=0.1
    )

    trainer = GRPOTrainer(
        model=model,
        reward_funcs=[correctness_reward_func, format_reward_func],
        args=training_args,
        train_dataset=train_dataset,
        processing_class=tokenizer,
        peft_config=grpo_peft_config,
    )

    print("Starting GRPO Training...")
    trainer.train()
    
    print("Saving GRPO Adapter...")
    trainer.save_model(args.output_path)
    wandb.finish()

if __name__ == "__main__":
    main()