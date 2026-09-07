def generate_isear_report(
    model_name,
    accuracy,
    total_samples,
    correct_predictions,
    incorrect_predictions,
    average_confidence,
    correct_confidence,
    incorrect_confidence,
    emotion_results,
    consistency=None
):
    """
    Generate a structured ISEAR benchmark report.
    """

    report = {
        "model": model_name,
        "total_samples": total_samples,
        "correct_predictions": correct_predictions,
        "incorrect_predictions": incorrect_predictions,
        "accuracy": accuracy,
        "average_confidence": average_confidence,
        "average_confidence_correct": correct_confidence,
        "average_confidence_incorrect": incorrect_confidence,
        "emotion_wise_results": emotion_results
    }

    if consistency is not None:
        report["model_consistency"] = consistency

    return report