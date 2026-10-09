
from unittest.mock import MagicMock

import pytest

import dashboard.app as dashboard_module


@pytest.fixture
def dashboard_client(monkeypatch):
    """Create a Flask test client with mocked application dependencies."""

    app = dashboard_module.app
    app.config["TESTING"] = True

    pipeline = MagicMock()
    history = MagicMock()
    recommendation_engine = MagicMock()

    history.get_emotional_history.return_value = []
    history.get_recommendation_history.return_value = []

    recommendation_engine.generate_recommendations.return_value = []

    monkeypatch.setattr(dashboard_module, "pipeline", pipeline)
    monkeypatch.setattr(dashboard_module, "history", history)
    monkeypatch.setattr(
        dashboard_module,
        "recommendation_engine",
        recommendation_engine,
    )

    client = app.test_client()

    return {
        "client": client,
        "pipeline": pipeline,
        "history": history,
        "engine": recommendation_engine,
    }


def sample_analysis_result():
    return {
        "text": "I feel hopeful today.",
        "preprocessed_text": "feel hopeful today",
        "sentiment": {
            "sentiment": "Positive",
            "compound": 0.7,
        },
        "emotions": {
            "emotions": {
                "joy": 0.85,
                "sadness": 0.05,
                "anger": 0.02,
                "fear": 0.03,
                "surprise": 0.03,
                "disgust": 0.02,
            },
            "detected_emotions": ["joy"],
            "primary_emotion": "joy",
            "primary_confidence": 0.85,
        },
        "intensity": {
            "intensity": 0.85,
            "severity": "High",
        },
        "emotional_state": {
            "emotional_state": "Positive",
            "dominant_emotion": "joy",
        },
    }


def sample_emotional_record():
    return {
        "timestamp": "2026-10-09T12:00:00",
        "emotional_state": {
            "emotional_state": "Positive",
            "dominant_emotion": "joy",
        },
        "intensity": {
            "intensity": 0.85,
            "severity": "High",
        },
    }


def sample_recommendation():
    return {
        "content": {
            "id": "gratitude_01",
            "title": "Practice Gratitude",
            "description": "Write down three things you appreciate.",
        },
        "score": 0.9,
        "explanation": ["Matches the detected positive emotion"],
    }


def test_dashboard_get_returns_success(dashboard_client):
    response = dashboard_client["client"].get("/")

    assert response.status_code == 200
    assert b"Mood Mentor" in response.data
    assert b"How are you feeling today?" in response.data
    assert b"Not analyzed" in response.data


def test_empty_mood_submission_shows_validation(dashboard_client):
    response = dashboard_client["client"].post(
        "/",
        data={"mood_text": "   "},
    )

    assert response.status_code == 200
    assert b"Please enter some text." in response.data
    dashboard_client["pipeline"].analyze.assert_not_called()


def test_valid_mood_submission_renders_analysis_and_recommendations(
    dashboard_client,
    monkeypatch,
):
    deps = dashboard_client

    deps["pipeline"].analyze.return_value = sample_analysis_result()
    deps["history"].get_emotional_history.return_value = [
        sample_emotional_record()
    ]
    deps["engine"].generate_recommendations.return_value = [
        sample_recommendation()
    ]

    monkeypatch.setattr(
        dashboard_module,
        "analyze_emotional_trends",
        lambda records: {"total_analyses": len(records)},
    )
    monkeypatch.setattr(
        dashboard_module,
        "determine_user_state",
        lambda trends: {
            "dominant_emotion": "joy",
            "trend": "Stable",
            "average_intensity": 0.85,
            "state": "Positive",
        },
    )

    response = deps["client"].post(
        "/",
        data={"mood_text": "I feel hopeful today."},
    )

    assert response.status_code == 200
    assert b"Your Emotional Analysis" in response.data
    assert b"Positive" in response.data
    assert b"Practice Gratitude" in response.data

    deps["pipeline"].analyze.assert_called_once_with(
        "I feel hopeful today."
    )
    deps["history"].add_emotional_record.assert_called_once()
    deps["engine"].generate_recommendations.assert_called_once()


def test_activity_history_renders_saved_records(dashboard_client):
    dashboard_client["history"].get_emotional_history.return_value = [
        sample_emotional_record()
    ]

    response = dashboard_client["client"].get("/activity-history")

    assert response.status_code == 200
    assert b"Analysis History" in response.data
    assert b"Positive" in response.data
    assert b"joy" in response.data
    assert b"1 Analyses" in response.data


def test_feedback_submission_records_acceptance_and_rating(
    dashboard_client,
):
    response = dashboard_client["client"].post(
        "/feedback",
        data={
            "recommendation_id": "gratitude_01",
            "feedback_type": "accepted",
            "rating": "5",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    dashboard_client["engine"].feedback.record_feedback.assert_called_once_with(
        recommendation_id="gratitude_01",
        viewed=True,
        accepted=True,
        rejected=False,
        rating=5,
    )


def test_missing_recommendation_id_redirects_without_recording_feedback(
    dashboard_client,
):
    response = dashboard_client["client"].post(
        "/feedback",
        data={"feedback_type": "accepted", "rating": "5"},
    )

    assert response.status_code == 302
    dashboard_client["engine"].feedback.record_feedback.assert_not_called()




def test_oversized_mood_entry_is_rejected(dashboard_client):
    response = dashboard_client["client"].post(
        "/",
        data={"mood_text": "a" * 5001},
    )

    assert response.status_code == 200
    assert b"5,000 characters" in response.data
    dashboard_client["pipeline"].analyze.assert_not_called()


def test_analysis_error_does_not_expose_exception(dashboard_client):
    dashboard_client["pipeline"].analyze.side_effect = RuntimeError(
        "sensitive internal database detail"
    )

    response = dashboard_client["client"].post(
        "/",
        data={"mood_text": "I feel stressed today."},
    )

    assert response.status_code == 200
    assert b"Please try again." in response.data
    assert b"sensitive internal database detail" not in response.data


def test_unknown_recommendation_id_is_rejected(dashboard_client):
    response = dashboard_client["client"].post(
        "/feedback",
        data={
            "recommendation_id": "unknown_999",
            "feedback_type": "accepted",
            "rating": "5",
        },
    )

    assert response.status_code == 302
    dashboard_client["engine"].feedback.record_feedback.assert_not_called()


def test_invalid_feedback_type_is_rejected(dashboard_client):
    response = dashboard_client["client"].post(
        "/feedback",
        data={
            "recommendation_id": "gratitude_01",
            "feedback_type": "something_else",
            "rating": "5",
        },
    )

    assert response.status_code == 302
    dashboard_client["engine"].feedback.record_feedback.assert_not_called()


@pytest.mark.parametrize("rating", ["0", "6", "-1", "abc"])
def test_invalid_rating_is_rejected(dashboard_client, rating):
    response = dashboard_client["client"].post(
        "/feedback",
        data={
            "recommendation_id": "gratitude_01",
            "feedback_type": "accepted",
            "rating": rating,
        },
    )

    assert response.status_code == 302
    dashboard_client["engine"].feedback.record_feedback.assert_not_called()


def test_feedback_without_rating_is_allowed(dashboard_client):
    response = dashboard_client["client"].post(
        "/feedback",
        data={
            "recommendation_id": "gratitude_01",
            "feedback_type": "rejected",
            "rating": "",
        },
    )

    assert response.status_code == 302
    dashboard_client["engine"].feedback.record_feedback.assert_called_once_with(
        recommendation_id="gratitude_01",
        viewed=True,
        accepted=False,
        rejected=True,
        rating=None,
    )
