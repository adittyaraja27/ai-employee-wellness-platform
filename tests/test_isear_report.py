from reports.isear_report import generate_isear_report


def test_isear_report():

    report = generate_isear_report(
        model_name="BERT",
        accuracy=0.4899,
        total_samples=5395,
        correct_predictions=2643,
        incorrect_predictions=2752,
        average_confidence=0.6999,
        correct_confidence=0.7873,
        incorrect_confidence=0.6161,
        emotion_results={
            "joy": 0.7372,
            "sadness": 0.7190,
            "anger": 0.4968,
            "fear": 0.3773,
            "disgust": 0.1107
        }
    )

    print("\nISEAR Report:")
    print(report)

    assert report["model"] == "BERT"
    assert report["total_samples"] == 5395
    assert report["correct_predictions"] == 2643
    assert report["incorrect_predictions"] == 2752
    assert "emotion_wise_results" in report

    print("\nISEAR REPORT TEST PASSED")


if __name__ == "__main__":
    test_isear_report()