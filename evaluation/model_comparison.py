BERT_RESULTS = {
    "accuracy": 0.7500,
    "precision": 0.7824,
    "recall": 0.6348,
    "macro_f1": 0.6951
}

DISTILBERT_RESULTS = {
    "accuracy": 0.7437,
    "precision": 0.7985,
    "recall": 0.5998,
    "macro_f1": 0.6714
}


def compare_models():

    print("\nBERT vs DistilBERT")
    print("-" * 50)

    print(f"{'Metric':<15} {'BERT':<12} {'DistilBERT':<12}")

    print(
        f"{'Accuracy':<15} "
        f"{BERT_RESULTS['accuracy']:.4f}      "
        f"{DISTILBERT_RESULTS['accuracy']:.4f}"
    )

    print(
        f"{'Precision':<15} "
        f"{BERT_RESULTS['precision']:.4f}      "
        f"{DISTILBERT_RESULTS['precision']:.4f}"
    )

    print(
        f"{'Recall':<15} "
        f"{BERT_RESULTS['recall']:.4f}      "
        f"{DISTILBERT_RESULTS['recall']:.4f}"
    )

    print(
        f"{'Macro F1':<15} "
        f"{BERT_RESULTS['macro_f1']:.4f}      "
        f"{DISTILBERT_RESULTS['macro_f1']:.4f}"
    )

    print("\nOverall:")
    print("BERT performs better on accuracy, recall and Macro F1.")
    print("DistilBERT performs better on precision.")


if __name__ == "__main__":
    compare_models()