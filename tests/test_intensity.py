from emotion.intensity import calculate_intensity


def test_intensity():

    emotion_scores = {
        "joy": 0.82,
        "sadness": 0.12,
        "anger": 0.05,
        "fear": 0.74,
        "surprise": 0.20,
        "disgust": 0.03
    }

    result = calculate_intensity(emotion_scores)

    print("\nIntensity Test")
    print("--------------------")
    print("Dominant Emotion:", result["dominant_emotion"])
    print("Intensity:", result["intensity"])
    print("Severity:", result["severity"])

    assert result["dominant_emotion"] == "joy"
    assert result["intensity"] == 0.82
    assert result["severity"] == "High"

    print("\nINTENSITY TEST PASSED")


if __name__ == "__main__":
    test_intensity()