from emotion.confidence import calculate_confidence


def test_confidence():
    logits = [3.0, -2.0, 1.5, -1.0, 0.5, -3.0]

    result = calculate_confidence(logits)

    print("\nEmotion probabilities:")

    for emotion, confidence in result["emotions"].items():
        print(f"{emotion}: {confidence:.4f}")

    print("\nDetected emotions:")
    print(result["detected_emotions"])

    print("\nPrimary emotion:")
    print(result["primary_emotion"])

    print("\nPrimary confidence:")
    print(f"{result['primary_confidence']:.4f}")

    assert "emotions" in result
    assert "primary_emotion" in result
    assert "primary_confidence" in result
    assert len(result["emotions"]) == 6

    assert 0 <= result["primary_confidence"] <= 1


if __name__ == "__main__":
    test_confidence()
    print("\nCONFIDENCE TEST PASSED")