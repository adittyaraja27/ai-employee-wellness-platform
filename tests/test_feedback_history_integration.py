from user.history import UserHistory
from recommendation.feedback import RecommendationFeedback


def test_feedback_history_integration():

    history = UserHistory()

    feedback = RecommendationFeedback(history)

    feedback.record_feedback(
        recommendation_id="walk_01",
        viewed=True,
        accepted=True,
        rating=5
    )

    feedback.record_feedback(
        recommendation_id="walk_01",
        viewed=True,
        accepted=True,
        rating=4
    )

    feedback.record_feedback(
        recommendation_id="break_01",
        viewed=True,
        accepted=False,
        rejected=True,
        rating=2
    )

    print("\nFeedback + UserHistory Integration Test")
    print("----------------------------------------")

    history_records = history.get_recommendation_history()

    print("Total history records:", len(history_records))

    acceptance_rate = feedback.calculate_acceptance_rate(
        "walk_01"
    )

    average_rating = feedback.calculate_average_rating(
        "walk_01"
    )

    feedback_score = feedback.calculate_feedback_score(
        "walk_01"
    )

    print("Walk acceptance rate:", acceptance_rate)
    print("Walk average rating:", average_rating)
    print("Walk feedback score:", feedback_score)

    assert len(history_records) == 3

    assert acceptance_rate == 1.0

    assert average_rating == 4.5

    assert feedback_score > 0

    print("\nFEEDBACK HISTORY INTEGRATION TEST PASSED")


if __name__ == "__main__":
    test_feedback_history_integration()