import torch
from transformers import AutoModelForSequenceClassification, Trainer

from training.dataset import prepare_dataset
from evaluation.metrics import calculate_metrics

MODEL_PATH= "models/distilbert"

def evaluate_distilbert():
    dataset, tokenizer= prepare_dataset()
    model=AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    model.to(device)
    validation_dataset=dataset["validation"]
    trainer = Trainer(
        model=model,
        processing_class=tokenizer
    )
    print(f"Evaluation device: {device}")
    print("Evaluating DistilBERT...")

    predictions = trainer.predict(validation_dataset)

    results= calculate_metrics(
        predictions.predictions,
        predictions.label_ids
    )
    print("\nDistilBERT Evaluation Results: ")
    for metric, value in results.items():
        print(f"{metric}: {value:.4f}")

if __name__=="__main__":
    evaluate_distilbert()