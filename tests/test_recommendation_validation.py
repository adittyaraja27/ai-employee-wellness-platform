from recommendation.hybrid import HybridRecommendationEngine


def test_recommendation_validation():

    engine = HybridRecommendationEngine()

    emotion_result = {
        "primary_emotion": "fear"
    }

    intensity_result = {
        "severity": "High"
    }

    user_preferences = {
        "activities": ["walking"],
        "content_types": [],
        "interests": []
    }

    user_text = (
        "I am extremely anxious and worried about my upcoming "
        "presentation and cannot concentrate."
    )

    recommendations = engine.generate_recommendations(
        user_text=user_text,
        emotion_result=emotion_result,
        intensity_result=intensity_result,
        user_preferences=user_preferences
    )

    print("\n=== RECOMMENDATION VALIDATION ===")

    assert len(recommendations) > 0

    for item in recommendations:

        print(
            f"\n{item['content']['title']}"
        )

        print(
            f"Score: {item['score']}"
        )

        print(
            f"Semantic similarity: "
            f"{item['semantic_similarity']}"
        )

        print(
            f"Breakdown: "
            f"{item['score_breakdown']}"
        )

        print(
            f"Explanation: "
            f"{item['explanation']}"
        )

        # Every recommendation should have an explanation
        assert len(item["explanation"]) > 0

        # Semantic matching must contribute
        assert item["score_breakdown"]["semantic_score"] >= 0

    # ------------------------------------------------
    # Verify recommendations are sorted by score
    # ------------------------------------------------

    scores = [
        item["score"]
        for item in recommendations
    ]

    assert scores == sorted(
        scores,
        reverse=True
    )

    # ------------------------------------------------
    # Verify emotion + intensity matching
    # ------------------------------------------------

    fear_high_matches = [
        item
        for item in recommendations
        if (
            item["content"]["id"] == "breathing_01"
            or item["content"]["id"] == "break_01"
        )
    ]

    assert len(fear_high_matches) > 0

    for item in fear_high_matches:

        breakdown = item["score_breakdown"]

        assert breakdown["emotion_score"] == 4
        assert breakdown["intensity_score"] == 3

    # ------------------------------------------------
    # Verify walking preference
    # ------------------------------------------------

    walking = next(
        item
        for item in recommendations
        if item["content"]["id"] == "walk_01"
    )

    assert walking["score_breakdown"]["preference_score"] >= 2

    print("\nRECOMMENDATION VALIDATION PASSED")


if __name__ == "__main__":
    test_recommendation_validation()
