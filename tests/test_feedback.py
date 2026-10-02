from recommendation.feedback import RecommendationFeedback


def test_feedback():

    feedback = RecommendationFeedback()

    # Record feedback for break_01
    feedback.record_feedback(
        recommendation_id="break_01",
        viewed=True,
        accepted=True,
        rating=5
    )

    feedback.record_feedback(
        recommendation_id="break_01",
        viewed=True,
        accepted=False,
        rejected=True,
        rating=2
    )

    feedback.record_feedback(
        recommendation_id="break_01",
        viewed=True,
        accepted=True,
        rating=4
    )

    print("\nRecommendation Feedback Test")
    print("-----------------------------")

    history = feedback.get_feedback_history()

    print("Total feedback:", len(history))

    acceptance_rate = feedback.calculate_acceptance_rate(
        "break_01"
    )

    average_rating = feedback.calculate_average_rating(
        "break_01"
    )

    print("Acceptance rate:", acceptance_rate)
    print("Average rating:", average_rating)

    # Assertions
    assert len(history) == 3

    assert acceptance_rate == 2 / 3

    assert average_rating == 11 / 3

    feedback_score = feedback.calculate_feedback_score(
    "break_01"
    )

    print("Feedback score:", feedback_score)

    assert -1.0 <= feedback_score <= 1.0
    print("\nFEEDBACK TEST PASSED")


if __name__ == "__main__":
    test_feedback()