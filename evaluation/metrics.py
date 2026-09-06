import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def calculate_metrics(logits, labels, threshold=0.5):
    """
    Calculate evaluation metrics for multi-label emotion classification.
    """

    logits = np.asarray(logits)
    labels = np.asarray(labels)

    probabilities = 1 / (1 + np.exp(-logits))
    predictions = (probabilities >= threshold).astype(int)

    accuracy = accuracy_score(labels, predictions)

    precision = precision_score(
        labels,
        predictions,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        labels,
        predictions,
        average="macro",
        zero_division=0
    )

    macro_f1 = f1_score(
        labels,
        predictions,
        average="macro",
        zero_division=0
    )

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "macro_f1": float(macro_f1)
    }