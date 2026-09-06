from datasets import load_dataset
from transformers import AutoTokenizer

from emotion.labels import EMOTION_LABELS, LABEL_TO_ID


DATASET_NAME = "AiLab-IMCS-UL/go_emotions-en"
MODEL_NAME = "bert-base-uncased"
MAX_LENGTH = 128


DATASET_LABELS = [
    "anger",
    "disgust",
    "fear",
    "joy",
    "sadness",
    "surprise",
    "neutral"
]


def convert_labels(example):
    """
    Convert GoEmotions Ekman labels into a
    six-dimensional multi-label vector.
    """

    label_vector = [0.0] * len(EMOTION_LABELS)

    for label_id in example["labels_ekman"]:
        label_name = DATASET_LABELS[label_id]

        if label_name in LABEL_TO_ID:
            label_vector[LABEL_TO_ID[label_name]] = 1.0

    example["emotion_labels"] = label_vector

    return example


def tokenize_dataset(dataset, tokenizer):
    """
    Tokenize text for BERT.
    """

    return dataset.map(
        lambda examples: tokenizer(
            examples["text"],
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH
        ),
        batched=True
    )


def prepare_dataset():
    """
    Load, filter, convert and tokenize the GoEmotions dataset.
    """

    dataset = load_dataset(DATASET_NAME)

    # Remove neutral examples.
    dataset = dataset.filter(
        lambda example: 6 not in example["labels_ekman"]
    )

    # Preserve original GoEmotions labels.
    dataset = dataset.rename_column("labels", "original_labels")

    # Create our six-emotion labels.
    dataset = dataset.map(convert_labels)

    # Load BERT tokenizer.
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Tokenize text.
    tokenized_dataset = tokenize_dataset(dataset, tokenizer)

    # Rename our six-emotion labels to the name expected by Trainer.
    tokenized_dataset = tokenized_dataset.rename_column(
        "emotion_labels",
        "labels"
    )

    return tokenized_dataset, tokenizer
