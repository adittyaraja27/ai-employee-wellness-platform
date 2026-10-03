from recommendation.explainability import generate_explanation


def test_explainability():

    content = {
        "id": "breathing_01",
        "title": "5-Minute Breathing Exercise"
    }

    score_breakdown = {
        "emotion_score": 4,
        "intensity_score": 3,
        "preference_score": 0,
        "semantic_score": 2.4,
        "feedback_score": 0.6,
        "final_score": 10.0
    }

    explanation = generate_explanation(
        content=content,
        primary_emotion="sadness",
        intensity="moderate",
        score_breakdown=score_breakdown
    )

    print("\n=== EXPLAINABILITY TEST ===")

    for reason in explanation:
        print("-", reason)

    print("===========================\n")

    assert len(explanation) > 0
    assert "sadness" in explanation[0]
    assert any(
        "intensity" in reason
        for reason in explanation
    )


if __name__ == "__main__":
    test_explainability()
    print("EXPLAINABILITY TEST PASSED")