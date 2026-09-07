from integration.mood_mentor_pipeline import MoodMentorPipeline


def test_mood_mentor_pipeline():
    pipeline = MoodMentorPipeline()

    text = (
        "I am excited about my promotion, "
        "but I am also nervous about the new responsibilities."
    )

    result = pipeline.analyze(text)

    # Basic output checks
    assert result["text"] == text
    assert result["preprocessed_text"]

    # Sentiment checks
    assert "sentiment" in result
    assert "compound" in result["sentiment"]
    assert result["sentiment"]["sentiment"] in [
        "Positive",
        "Negative",
        "Neutral"
    ]

    # Emotion checks
    assert "emotions" in result
    assert "emotions" in result["emotions"]
    assert "detected_emotions" in result["emotions"]
    assert "primary_emotion" in result["emotions"]
    assert "primary_confidence" in result["emotions"]

    # Confidence must be valid
    assert 0.0 <= result["emotions"]["primary_confidence"] <= 1.0

    print("\nMOOD MENTOR INTEGRATION TEST PASSED")


if __name__ == "__main__":
    test_mood_mentor_pipeline()
