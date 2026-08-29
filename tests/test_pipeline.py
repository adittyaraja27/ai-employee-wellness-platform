from ingestion.text_ingestion import (
    read_text_input,
    read_txt_file,
    read_csv_file,
    validate_text
)

from preprocessing.text_preprocessor import preprocess_text

from sentiment.vader_analyzer import analyze_sentiment

from reports.sentiment_report import generate_sentiment_report


def process_text(text):
    """
    Complete pipeline for a single text input.
    """

    # Step 1: Validate input
    if not validate_text(text):
        raise ValueError("Invalid text input")

    # Step 2: Preprocess
    processed_text = preprocess_text(text)

    if not processed_text:
        raise ValueError("Preprocessing produced empty text")

    # Step 3: Sentiment analysis
    sentiment_result = analyze_sentiment(text)

    # Step 4: Combine results
    return {
        "input_text": text,
        "processed_text": processed_text,
        "sentiment": sentiment_result["sentiment"],
        "positive": sentiment_result["positive"],
        "negative": sentiment_result["negative"],
        "neutral": sentiment_result["neutral"],
        "compound": sentiment_result["compound"]
    }


def test_direct_text_pipeline():

    text = read_text_input(
        "I am feeling happy and productive today!"
    )

    result = process_text(text)

    print("\nDIRECT TEXT PIPELINE")
    print(result)

    assert result["input_text"] == text
    assert result["processed_text"] != ""
    assert result["sentiment"] in ["Positive", "Negative", "Neutral"]


def test_txt_pipeline():

    text = read_txt_file("data/sample.txt")

    result = process_text(text)

    print("\nTXT PIPELINE")
    print(result)

    assert validate_text(text)
    assert result["processed_text"] != ""
    assert result["sentiment"] in ["Positive", "Negative", "Neutral"]


def test_csv_pipeline():

    texts = read_csv_file("data/sample.csv")

    results = []

    for text in texts:

        result = process_text(text)

        results.append(result)

    report, summary = generate_sentiment_report(results)

    print("\nCSV PIPELINE")
    print(report.to_string(index=False))

    print("\nSUMMARY")
    print(summary)

    assert len(results) == len(texts)
    assert summary["total_samples"] == len(texts)
    assert (
        summary["positive"]
        + summary["negative"]
        + summary["neutral"]
        == summary["total_samples"]
    )


def test_invalid_input_pipeline():

    invalid_inputs = [
        "",
        "     ",
        None
    ]

    for text in invalid_inputs:

        try:
            process_text(text)

            assert False, f"Invalid input was accepted: {repr(text)}"

        except ValueError:

            print(
                "Correctly rejected:",
                repr(text)
            )


if __name__ == "__main__":

    test_direct_text_pipeline()
    test_txt_pipeline()
    test_csv_pipeline()
    test_invalid_input_pipeline()

    print("\nALL PIPELINE TESTS PASSED")