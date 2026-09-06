import numpy as np

from emotion.labels import EMOTION_LABELS


DEFAULT_THRESHOLD = 0.5


def sigmoid(logits):
    """
    Convert model logits into independent probabilities.
    """
    return 1 / (1 + np.exp(-logits))


def calculate_confidence(logits, threshold=DEFAULT_THRESHOLD):
    """
    Calculate confidence scores for all emotions.

    Returns:
        - probabilities for every emotion
        - detected emotions based on threshold
        - primary emotion
        - primary confidence
        - threshold used
    """

    probabilities = sigmoid(np.asarray(logits))

    if probabilities.ndim != 1:
        probabilities = probabilities.flatten()

    if len(probabilities) != len(EMOTION_LABELS):
        raise ValueError(
            f"Expected {len(EMOTION_LABELS)} scores, "
            f"but received {len(probabilities)}."
        )

    emotion_scores = {
        emotion: float(probability)
        for emotion, probability in zip(
            EMOTION_LABELS,
            probabilities
        )
    }

    detected_emotions = [
        emotion
        for emotion, probability in emotion_scores.items()
        if probability >= threshold
    ]

    primary_emotion = max(
        emotion_scores,
        key=emotion_scores.get
    )

    primary_confidence = emotion_scores[primary_emotion]

    return {
        "emotions": emotion_scores,
        "detected_emotions": detected_emotions,
        "primary_emotion": primary_emotion,
        "primary_confidence": primary_confidence,
        "threshold": threshold
    }