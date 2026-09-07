import numpy as np
import torch

from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from emotion.labels import EMOTION_LABELS


ISEAR_DATASET = "gsri-18/ISEAR-dataset-complete"

MODEL_PATHS = {
    "BERT": "models/bert",
    "DistilBERT": "models/distilbert"
}

SUPPORTED_LABELS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "disgust"
]


def sigmoid(logits):
    return 1 / (1 + np.exp(-logits))


def load_isear():
    dataset = load_dataset(ISEAR_DATASET)
    return dataset["train"]


def evaluate_model(model_name, model_path, dataset):

    print(f"\nEvaluating {model_name}...")

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    model = AutoModelForSequenceClassification.from_pretrained(
        model_path
    )

    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    model.to(device)
    model.eval()

    predictions = []
    true_labels = []
    confidences = []
    incorrect_predictions = []

    for example in dataset:

        text = example["content"]
        emotion = example["emotion"].lower().strip()

        if emotion not in SUPPORTED_LABELS:
            continue

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = sigmoid(
            outputs.logits.detach().cpu().numpy()[0]
        )

        predicted_index = int(np.argmax(probabilities))
        predicted_emotion = EMOTION_LABELS[predicted_index]

        confidence = float(probabilities[predicted_index])

        predictions.append(predicted_emotion)
        true_labels.append(emotion)
        confidences.append(confidence)

        if predicted_emotion != emotion:
            incorrect_predictions.append({
                "text": text,
                "true": emotion,
                "predicted": predicted_emotion,
                "confidence": confidence
            })

    return {
        "predictions": predictions,
        "true_labels": true_labels,
        "confidences": confidences,
        "incorrect_predictions": incorrect_predictions
    }


def calculate_accuracy(predictions, true_labels):

    correct = sum(
        prediction == true
        for prediction, true in zip(predictions, true_labels)
    )

    return correct / len(true_labels)


def print_results(model_name, results):

    predictions = results["predictions"]
    true_labels = results["true_labels"]
    confidences = results["confidences"]
    incorrect = results["incorrect_predictions"]

    accuracy = calculate_accuracy(
        predictions,
        true_labels
    )

    print(f"\n{model_name} ISEAR Results")
    print("-" * 50)

    print(f"Samples evaluated: {len(true_labels)}")
    print(f"Correct predictions: {len(true_labels) - len(incorrect)}")
    print(f"Incorrect predictions: {len(incorrect)}")
    print(f"Accuracy: {accuracy:.4f}")

    print(
        f"Average confidence: "
        f"{np.mean(confidences):.4f}"
    )

    print(
        f"Average confidence on correct predictions: "
        f"{np.mean([c for c, p, t in zip(confidences, predictions, true_labels) if p == t]):.4f}"
    )

    print(
        f"Average confidence on incorrect predictions: "
        f"{np.mean([c for c, p, t in zip(confidences, predictions, true_labels) if p != t]):.4f}"
    )

    print("\nEmotion-wise results:")

    for emotion in SUPPORTED_LABELS:

        total = sum(
            true == emotion
            for true in true_labels
        )

        correct = sum(
            prediction == true == emotion
            for prediction, true in zip(
                predictions,
                true_labels
            )
        )

        accuracy = correct / total if total else 0

        print(
            f"{emotion:<10}"
            f"{correct}/{total}"
            f" ({accuracy:.4f})"
        )

    print("\nSample incorrect predictions:")

    for item in incorrect[:5]:

        print(
            f"\nTrue: {item['true']}"
            f"\nPredicted: {item['predicted']}"
            f"\nConfidence: {item['confidence']:.4f}"
            f"\nText: {item['text'][:150]}"
        )


def calculate_consistency(bert_results, distilbert_results):

    bert_predictions = bert_results["predictions"]
    distil_predictions = distilbert_results["predictions"]

    matching = sum(
        bert == distil
        for bert, distil in zip(
            bert_predictions,
            distil_predictions
        )
    )

    consistency = matching / len(bert_predictions)

    return consistency


def main():

    dataset = load_isear()

    print(f"ISEAR samples: {len(dataset)}")

    all_results = {}

    for model_name, model_path in MODEL_PATHS.items():

        results = evaluate_model(
            model_name,
            model_path,
            dataset
        )

        all_results[model_name] = results

        print_results(
            model_name,
            results
        )

    consistency = calculate_consistency(
        all_results["BERT"],
        all_results["DistilBERT"]
    )

    print("\nModel Consistency")
    print("-" * 50)
    print(
        f"BERT vs DistilBERT agreement: "
        f"{consistency:.4f}"
    )


if __name__ == "__main__":
    main()