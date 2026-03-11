import io
import sys
import torch
import transformers
from typing import Tuple, Optional, Any, List, Union

def model_evaluation(model, tokenizer, system_content, question, max_new_tokens, n_samples = 5, temperature = 0.5, top_p = 0.7):
    """
    added n_samples, temperature, and top_p for Q5.
    Args:
        model:
        tokenizer:
        system_content:
        question:
        max_new_tokens:
        n_samples:
        temperature:
        top_p:

    Returns:

    """
    instruction = (

        "Think step by step before answering the question, and provide the final answer "
        "as 'the answer is [answer]' format."
    )

    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": question},
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )

    input_ids = inputs.to(model.device)
    attention_mask = torch.ones_like(input_ids).to(model.device)

    output_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
        num_return_sequences=n_samples,
        pad_token_id=tokenizer.pad_token_id,
    )

    completions = []
    prompt_len = input_ids.shape[1]

    for seq in output_ids:
        text = tokenizer.decode(seq[prompt_len:], skip_special_tokens=True)
        completions.append(text)

    return completions
