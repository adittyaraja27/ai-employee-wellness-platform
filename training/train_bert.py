import numpy as np
import torch

from transformers import (
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

from training.dataset import prepare_dataset
from emotion.labels import EMOTION_LABELS


MODEL_NAME = "bert-base-uncased"
OUTPUT_DIR = "models/bert"


def compute_metrics(eval_prediction):
    """
    Calculate multi-label accuracy.
    """

    logits = eval_prediction.predictions
    labels = eval_prediction.label_ids

    probabilities = 1 / (1 + np.exp(-logits))
    predictions = (probabilities >= 0.5).astype(int)

    accuracy = (predictions == labels).mean()

    return {
        "accuracy": float(accuracy)
    }


def train_bert():
    """
    Fine-tune BERT for six-emotion multi-label classification.
    """

    dataset, tokenizer = prepare_dataset()

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(EMOTION_LABELS),
        problem_type="multi_label_classification",
        id2label={
            index: label
            for index, label in enumerate(EMOTION_LABELS)
        },
        label2id={
            label: index
            for index, label in enumerate(EMOTION_LABELS)
        }
    )

    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    model.to(device)

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_steps=100,
        report_to="none"
    )
    # Small smoke-test dataset
    train_dataset = dataset["train"]
    validation_dataset = dataset["validation"]
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
	eval_dataset=validation_dataset,
        processing_class=tokenizer,
        compute_metrics=compute_metrics
    )

    print(f"Training device: {device}")
    print("Starting BERT training...")

    trainer.train()

    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("\nBERT training completed.")
    print(f"Model saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    train_bert()
