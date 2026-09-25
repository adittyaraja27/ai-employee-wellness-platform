from emotion.intensity import calculate_intensity
from emotion.emotional_state import analyze_emotional_state


def test_emotional_state():

    emotion_scores = {
        "joy": 0.82,
        "sadness": 0.12,
        "anger": 0.08,
        "fear": 0.74,
        "surprise": 0.10,
        "disgust": 0.03
    }

    intensity_result = calculate_intensity(emotion_scores)

    result = analyze_emotional_state(
        emotion_scores,
        intensity_result
    )

    print("\nEmotional State Test")
    print("-------------------------")
    print("Dominant:", result["dominant_emotion"])
    print("Secondary:", result["secondary_emotions"])
    print("Mixed:", result["is_mixed"])
    print("Polarity:", result["polarity"])
    print("State:", result["emotional_state"])
    print("Intensity:", result["intensity"])
    print("Severity:", result["severity"])

    assert result["dominant_emotion"] == "joy"
    assert "fear" in result["secondary_emotions"]
    assert result["is_mixed"] is True
    assert result["polarity"] == "Mixed"
    assert result["emotional_state"] == "Mixed emotional state"
    assert result["severity"] == "High"

    print("\nEMOTIONAL STATE TEST PASSED")


if __name__ == "__main__":
    test_emotional_state()