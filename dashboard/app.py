import traceback

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

                # Debug output
                print("\n=== RECOMMENDATIONS DEBUG ===")
                print(recommendations)
                print("============================\n")

            except Exception as e:

                traceback.print_exc()
                error = str(e)

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

    recommendation_id = request.form.get("recommendation_id")
    feedback_type = request.form.get("feedback_type")
    rating = request.form.get("rating")

    if not recommendation_id:
        return redirect(url_for("dashboard"))

    accepted = feedback_type == "accepted"
    rejected = feedback_type == "rejected"

    rating_value = None

    if rating:
        try:
            rating_value = int(rating)
        except ValueError:
            rating_value = None

    recommendation_engine.feedback.record_feedback(
        recommendation_id=recommendation_id,
        viewed=True,
        accepted=accepted,
        rejected=rejected,
        rating=rating_value
    )

    print("\n=== FEEDBACK DEBUG ===")
    print(
        recommendation_engine.feedback.get_recommendation_feedback(
            recommendation_id
        )
    )
    print(
        "Acceptance rate:",
        recommendation_engine.feedback.calculate_acceptance_rate(
            recommendation_id
        )
    )
    print(
        "Average rating:",
        recommendation_engine.feedback.calculate_average_rating(
            recommendation_id
        )
    )
    print(
        "Feedback score:",
        recommendation_engine.feedback.calculate_feedback_score(
            recommendation_id
        )
    )
    print("======================\n")

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5001
    )

@app.route("/feedback", methods=["POST"])
def recommendation_feedback():

    recommendation_id = request.form.get("recommendation_id")
    feedback_type = request.form.get("feedback_type")
    rating = request.form.get("rating")

    if not recommendation_id:
        return redirect(url_for("dashboard"))

    accepted = feedback_type == "accepted"
    rejected = feedback_type == "rejected"

    rating_value = None

    if rating:
        try:
            rating_value = int(rating)
        except ValueError:
            rating_value = None

    recommendation_engine.feedback.record_feedback(
        recommendation_id=recommendation_id,
        viewed=True,
        accepted=accepted,
        rejected=rejected,
        rating=rating_value
    )
    print("\n=== FEEDBACK DEBUG ===")
    print(
        recommendation_engine.feedback.get_recommendation_feedback(
            recommendation_id
        )
    )
    print(
        "Acceptance rate:",
        recommendation_engine.feedback.calculate_acceptance_rate(
            recommendation_id
        )
    )
    print(
        "Average rating:",
        recommendation_engine.feedback.calculate_average_rating(
            recommendation_id
        )
    )
    print(
        "Feedback score:",
        recommendation_engine.feedback.calculate_feedback_score(
            recommendation_id
        )
    )
    print("======================\n")
    
    return redirect(url_for("dashboard"))