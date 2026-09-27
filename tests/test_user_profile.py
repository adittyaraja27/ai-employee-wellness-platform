from user.profile import UserProfile
from user.history import UserHistory


def test_user_profile():

    profile = UserProfile("user_001")

    profile.update_preferences(
        activities=["breathing", "meditation"],
        content_types=["audio"],
        interests=["stress management"]
    )

    preferences = profile.get_preferences()

    assert preferences["activities"] == [
        "breathing",
        "meditation"
    ]

    assert preferences["content_types"] == ["audio"]

    assert preferences["interests"] == [
        "stress management"
    ]

    assert len(profile.get_preference_history()) == 1

    print("USER PROFILE TEST PASSED")


def test_user_history():

    history = UserHistory()

    history.add_emotional_record(
        emotions={"fear": 0.82},
        intensity=0.82,
        emotional_state="Negative emotional state"
    )

    history.add_recommendation_record(
        recommendation_id="breathing_001",
        viewed=True,
        accepted=True,
        rating=5
    )

    history.add_interaction("Completed breathing exercise")

    assert len(history.get_emotional_history()) == 1
    assert len(history.get_recommendation_history()) == 1
    assert len(history.get_interaction_history()) == 1

    print("USER HISTORY TEST PASSED")


if __name__ == "__main__":
    test_user_profile()
    test_user_history()