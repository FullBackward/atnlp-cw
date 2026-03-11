import random
import re
import json
from tqdm import tqdm
from utils import model_evaluation
import string
from math_verify import parse, verify
from collections import Counter

from decimal import Decimal, InvalidOperation

def normalize_answer_for_vote(answer):
    """
    Normalize lightly-decorated numeric answers so equivalent forms vote together.

    Examples:
        $42 -> 42
        42.0 -> 42
        42,000 -> 42000
    """
    if not answer or answer == "Invalid":
        return "Invalid"

    s = answer.strip().lower()

    # remove wrappers
    s = re.sub(r"^[\[\(\{]\s*", "", s)
    s = re.sub(r"\s*[\]\)\}]$", "", s)

    # remove leading currency sign
    s = re.sub(r"^\$", "", s)

    # remove trailing punctuation
    s = re.sub(r"[.,;:!?]+$", "", s).strip()

    # strict numeric-only normalization
    if not re.fullmatch(r"[-+]?\d[\d,]*\.?\d*", s):
        return s

    s = s.replace(",", "")

    try:
        value = Decimal(s)
    except InvalidOperation:
        return s

    if value == value.to_integral():
        return str(int(value))

    return format(value.normalize(), "f").rstrip("0").rstrip(".")


def extract_final_answer(model_result):
    """
    Extract the final answer in a way that matches the SFT / GRPO target format.

    Expected format:
        The answer is <answer>

    Returns:
        Extracted answer string if the target format is found, else "Invalid".
    """
    if not model_result:
        return "Invalid"

    matches = re.findall(
        r"(?i)\bthe answer is\b\s+(.+?)(?=[\n\r]|$)",
        model_result
    )
    if not matches:
        return "Invalid"

    final_answer = matches[-1].strip()

    # Remove simple wrappers like [42] or (42)
    final_answer = re.sub(r"^[\[\(\{]\s*", "", final_answer)
    final_answer = re.sub(r"\s*[\]\)\}]$", "", final_answer)

    # Remove trailing punctuation like "." or ","
    final_answer = re.sub(r"[.,;:!?]+$", "", final_answer).strip()

    return final_answer if final_answer else "Invalid"


def majority_vote(answers):
    valid_answers = [a for a in answers if a != "Invalid"]

    if not valid_answers:
        return "Invalid"

    counts = Counter(valid_answers)
    top_count = max(counts.values())
    top_answers = [ans for ans, count in counts.items() if count == top_count]

    # simple deterministic tie break, just pick first if there are multiple "top answers"
    return sorted(top_answers)[0]

def load_gsm8k_questions(dataset):
    questions = []
    for item in dataset:
        question = item['question']
        answer_match = re.search(r'####\s*(\d+)', item['answer'])
        if answer_match:
            answer = answer_match.group(1)
            questions.append({
                'question': question,
                'answer': answer
            })
    return questions

def process_gsm8k_questions(
    questions,
    output_file_path,
    formulation_prompt_path,
    model_type,
    model,
    tokenizer=None,
    device=None
):
    results = []
    total_correct = 0
    total_questions = 0
    valid_correct = 0
    valid_questions = 0

    for example in tqdm(questions, desc="Processing GSM8K questions"):
        question = example['question']
        correct_answer = example['answer']

        print(f"Processing question: {question}")

        model_results = model_evaluation(
            model,
            tokenizer,
            None,
            question,
            500,
            n_samples=5,
            temperature=0.5,
            top_p=0.7
        )

        print(f"Model result: {model_results}")
        candidate_answers_raw = [extract_final_answer(r) for r in model_results]
        candidate_answers = [normalize_answer_for_vote(a) for a in candidate_answers_raw]
        final_answer = majority_vote(candidate_answers)

        # Use math_verify to check correctness
        try:
            gold = parse(correct_answer)
            answer = parse(final_answer)
            is_correct = verify(gold, answer)
        except Exception as e:
            print(f"Error in math_verify: {e}")
            is_correct = False

        if is_correct:
            total_correct += 1
        total_questions += 1
        
        # Track valid answers separately
        if final_answer != "Invalid":
            valid_questions += 1
            if is_correct:
                valid_correct += 1

        result = {
            "question": question,
            "model_results": model_results,
            "candidate_answers_raw": candidate_answers_raw,
            "candidate_answers_normalized": candidate_answers,
            "final_answer": final_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
        }
        results.append(result)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Saved results for question {len(results)}")

    # Calculate all three accuracies
    overall_accuracy = total_correct / total_questions if total_questions > 0 else 0
    valid_accuracy = valid_correct / valid_questions if valid_questions > 0 else 0
    invalid_count = total_questions - valid_questions
    invalid_rate = invalid_count / total_questions if total_questions > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"Total questions: {total_questions}")
    print(f"Valid Accuracy (excluding invalid): {valid_accuracy:.2%}")
    
    return results, overall_accuracy, valid_accuracy, invalid_rate