from flask import Flask, render_template, request, redirect, url_for

from integration.mood_mentor_pipeline import MoodMentorPipeline
from user.history import UserHistory

from recommendation.hybrid import HybridRecommendationEngine
from recommendation.trend_analyzer import analyze_emotional_trends
from recommendation.user_state import determine_user_state


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
pipeline = MoodMentorPipeline()
history = UserHistory()
recommendation_engine = HybridRecommendationEngine(history)


@app.route("/", methods=["GET", "POST"])
def dashboard():

    result = None
    error = None
    text = ""
    recommendations = []
    trend_result = None
    user_state = None

    if request.method == "POST":

        text = request.form.get("mood_text", "").strip()

        if not text:
            error = "Please enter some text."
        elif len(text) > 5000:
            error = "Please limit your mood entry to 5,000 characters."

        else:
            try:

                # 1. Analyze current mood
                result = pipeline.analyze(text)

                # 2. Store emotional history
                history.add_emotional_record(
                    emotions=result["emotions"],
                    intensity=result["intensity"],
                    emotional_state=result["emotional_state"]
                )

                # 3. Analyze emotional trends
                trend_result = analyze_emotional_trends(
                    history.get_emotional_history()
                )

                # 4. Determine current user state
                user_state = determine_user_state(
                    trend_result
                )

                # 5. Generate hybrid recommendations
                recommendations = recommendation_engine.generate_recommendations(
                    user_text=text,
                    emotion_result=result["emotions"],
                    intensity_result=result["intensity"]
                )

                

            except Exception:
                app.logger.exception("Mood analysis failed.")
                error = (
                    "We couldn't analyze your entry right now. "
                    "Please try again."
                )

    return render_template(
        "dashboard.html",
        result=result,
        error=error,
        text=text,
        recommendations=recommendations,
        trend_result=trend_result,
        user_state=user_state
    )


@app.route("/activity-history")
def activity_history():

    records = history.get_emotional_history()

    return render_template(
        "activity_history.html",
        records=records
    )

@app.route("/feedback", methods=["POST"])
def recommendation_feedback():
    recommendation_id = request.form.get(
        "recommendation_id", ""
    ).strip()
    feedback_type = request.form.get("feedback_type", "")
    rating = request.form.get("rating", "").strip()

    valid_recommendation_ids = {
        "breathing_01",
        "break_01",
        "journaling_01",
        "gratitude_01",
        "walk_01",
    }

    if recommendation_id not in valid_recommendation_ids:
        return redirect(url_for("dashboard"))

    if feedback_type not in {"accepted", "rejected"}:
        return redirect(url_for("dashboard"))

    rating_value = None

    if rating:
        try:
            rating_value = int(rating)
        except ValueError:
            return redirect(url_for("dashboard"))

        if not 1 <= rating_value <= 5:
            return redirect(url_for("dashboard"))

    accepted = feedback_type == "accepted"
    rejected = feedback_type == "rejected"

    recommendation_engine.feedback.record_feedback(
        recommendation_id=recommendation_id,
        viewed=True,
        accepted=accepted,
        rejected=rejected,
        rating=rating_value,
    )

    return redirect(url_for("dashboard"))



if __name__ == "__main__":
    app.run(
        debug=False,
        port=5001
    )


