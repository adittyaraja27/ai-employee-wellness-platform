EMOTION_LABELS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust"
]

LABEL_TO_ID = {
    label: index for index, label in enumerate(EMOTION_LABELS)
}

ID_TO_LABEL = {
    index: label for index, label in enumerate(EMOTION_LABELS)
}

NUM_LABELS = len(EMOTION_LABELS)
