from integration.mood_mentor_pipeline import MoodMentorPipeline


def test_edge_cases():

    pipeline = MoodMentorPipeline()

    test_cases = [
        ("positive", "I got the job I wanted!"),
        ("negative", "Everything is going terribly today."),
        ("neutral", "The meeting is scheduled for tomorrow."),
        (
            "mixed",
            "I'm happy about the promotion but scared of the responsibility."
        ),
        ("short", "Great!"),
        (
            "long",
            "I have been thinking about my career, my future, "
            "my responsibilities, and all the changes happening "
            "around me. Sometimes I feel excited, but at other "
            "times I feel uncertain about what will happen next."
        ),
        ("informal", "ugh this day is sooo bad lol"),
        ("emoji", "I'm so happy today 😊🎉"),
        ("ambiguous", "Well... that was interesting.")
    ]

    for name, text in test_cases:

        result = pipeline.analyze(text)

        assert result["text"] == text
        assert result["preprocessed_text"]

        assert "sentiment" in result
        assert "emotions" in result

        assert result["emotions"]["primary_emotion"] in [
            "joy",
            "sadness",
            "anger",
            "fear",
            "surprise",
            "disgust"
        ]

        assert 0.0 <= result["emotions"]["primary_confidence"] <= 1.0

        print(f"PASS: {name}")


def test_invalid_inputs():

    pipeline = MoodMentorPipeline()

    invalid_inputs = [
        "",
        "   ",
        None,
        12345
    ]

    for value in invalid_inputs:

        try:
            pipeline.analyze(value)
            assert False, f"Expected ValueError for: {value!r}"

        except ValueError:
            print(f"PASS: invalid input {value!r}")


if __name__ == "__main__":

    test_edge_cases()
    test_invalid_inputs()

    print("\nALL EDGE CASE TESTS PASSED")
