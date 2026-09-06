import numpy as np

from evaluation.metrics import calculate_metrics


def test_evaluation():

    logits = np.array([
        [3.0, -2.0, 1.5, -1.0, 0.5, -3.0],
        [-2.0, 3.0, -1.5, 2.0, -2.0, -1.0],
        [-2.0, -1.0, 3.0, -2.0, -1.0, 2.5],
        [2.5, -2.0, -1.0, -2.0, 2.0, -2.0]
    ])

    labels = np.array([
        [1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0]
    ])

    results = calculate_metrics(logits, labels)

    print("\nEvaluation Results:")

    for metric, value in results.items():
        print(f"{metric}: {value:.4f}")

    assert 0 <= results["accuracy"] <= 1
    assert 0 <= results["precision"] <= 1
    assert 0 <= results["recall"] <= 1
    assert 0 <= results["macro_f1"] <= 1

    print("\nEVALUATION TEST PASSED")


if __name__ == "__main__":
    test_evaluation()