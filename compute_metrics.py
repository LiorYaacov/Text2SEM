import json
import re
from transformers import EvalPrediction

def extract_json(text):
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None

def compute_metrics(eval_preds: EvalPrediction):
    predictions, labels = eval_preds

    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    total = len(decoded_preds)
    exact_match = 0
    invalid = 0
    field_correct = {"action": 0, "shape": 0, "direction": 0, "distance": 0}

    for pred_str, label_str in zip(decoded_preds, decoded_labels):
        pred_json = extract_json(pred_str)
        label_json = extract_json(label_str)

        if pred_json is None or label_json is None:
            invalid += 1
            continue

        fields_match = all(
            str(pred_json.get(k)).lower() == str(label_json.get(k)).lower()
            for k in field_correct
        )
        if fields_match:
            exact_match += 1

        for k in field_correct:
            if str(pred_json.get(k)).lower() == str(label_json.get(k)).lower():
                field_correct[k] += 1

    return {
        "valid_json": (total - invalid) / total,
        "exact_match": exact_match / total,
        "action_acc": field_correct["action"] / total,
        "shape_acc": field_correct["shape"] / total,
        "direction_acc": field_correct["direction"] / total,
        "distance_acc": field_correct["distance"] / total
    }
