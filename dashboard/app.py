from user.history import UserHistory
from recommendation.personalized import generate_recommendations
from flask import Flask, render_template, request

from integration.mood_mentor_pipeline import MoodMentorPipeline


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static"
)


pipeline = MoodMentorPipeline()
history = UserHistory()


@app.route("/", methods=["GET", "POST"])
def dashboard():

    result = None
    error = None
    text = ""
    recommendations = []

    if request.method == "POST":

        text = request.form.get("mood_text", "").strip()

        if not text:
            error = "Please enter some text."

        else:
            try:
                result = pipeline.analyze(text)
                history.add_emotional_record(
                    emotions=result["emotions"],
                    intensity=result["intensity"],
                    emotional_state=result["emotional_state"]
                )
                recommendations = generate_recommendations(
                    result["emotions"],
                    result["intensity"]
                )

            except Exception as e:
                error = str(e)

    return render_template(
        "dashboard.html",
        result=result,
        error=error,
        text=text,
        recommendations=recommendations
    )
@app.route("/activity-history")
def activity_history():

    records = history.get_emotional_history()

    return render_template(
        "activity_history.html",
        records=records
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)