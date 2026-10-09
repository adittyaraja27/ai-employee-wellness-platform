import streamlit as st

from integration.mood_mentor_pipeline import MoodMentorPipeline
from user.history import UserHistory
from recommendation.hybrid import HybridRecommendationEngine
from recommendation.trend_analyzer import analyze_emotional_trends
from reports.wellness_report import (
    generate_wellness_report,
    generate_recommendation_csv
)

# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="Mood Mentor",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# Application Components
# ==================================================

@st.cache_resource
def load_pipeline():
    return MoodMentorPipeline()


@st.cache_resource
def load_history():
    return UserHistory()


@st.cache_resource
def load_recommendation_engine(_history):
    return HybridRecommendationEngine(_history)

pipeline = load_pipeline()
history = load_history()
recommendation_engine = load_recommendation_engine(history)


# ==================================================
# Session State
# ==================================================

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "latest_recommendations" not in st.session_state:
    st.session_state.latest_recommendations = []


# ==================================================
# Header
# ==================================================

st.title("🧠 Mood Mentor")

st.subheader(
    "AI-Based Employee Wellness Management Platform"
)

st.write(
    "Describe how you are feeling, and Mood Mentor will "
    "analyze your emotional state and provide personalized "
    "wellness recommendations."
)


# ==================================================
# Mood Input
# ==================================================

st.markdown("### How are you feeling?")

user_text = st.text_area(
    "Write about your current thoughts or feelings:",
    placeholder=(
        "Example: I have been feeling stressed "
        "about my workload today..."
    ),
    height=150
)


# ==================================================
# Analyze Mood
# ==================================================

if st.button("Analyze My Mood", type="primary"):

    if not user_text.strip():
        st.warning(
            "Please enter some text before analyzing."
        )
        st.stop()

    try:

        with st.spinner(
            "Analyzing your emotional state..."
        ):

            result = pipeline.analyze(user_text)

            recommendations = (
                recommendation_engine.generate_recommendations(
                    user_text=user_text,
                    emotion_result=result["emotions"],
                    intensity_result=result["intensity"]
                )
            )

        # ------------------------------------------
        # Save analysis in history
        # ------------------------------------------

        history.add_emotional_record(
            emotions=result["emotions"],
            intensity=result["intensity"],
            emotional_state=result["emotional_state"]
        )

        # ------------------------------------------
        # Store latest analysis in session state
        # ------------------------------------------

        st.session_state.latest_result = result
        st.session_state.latest_recommendations = (
            recommendations
        )

        st.success(
            "Analysis completed successfully."
        )

    except Exception as e:

        st.error(
            "An error occurred during analysis."
        )

        with st.expander("Technical Details"):
            st.code(str(e))


# ==================================================
# Display Latest Analysis
# ==================================================

result = st.session_state.latest_result
recommendations = (
    st.session_state.latest_recommendations
)


if result is not None:

    # ==================================================
    # Emotional Analysis
    # ==================================================

    st.markdown("## Emotional Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Sentiment",
            result["sentiment"]["sentiment"]
        )

    with col2:

        st.metric(
            "Emotional State",
            result["emotional_state"]["emotional_state"]
        )

    with col3:

        st.metric(
            "Intensity",
            result["intensity"]["severity"]
        )


    # ==================================================
    # Emotion Scores
    # ==================================================

    st.markdown("### Emotion Scores")

    emotions = result["emotions"]["emotions"]

    for emotion, score in emotions.items():

        st.write(
            f"**{emotion.capitalize()}** — {score:.1%}"
        )

        st.progress(
            float(score)
        )


    # ==================================================
    # Recommendations
    # ==================================================

    st.markdown(
        "## 💡 Personalized Recommendations"
    )

    if not recommendations:

        st.info(
            "No recommendations were generated."
        )

    else:

        for index, recommendation in enumerate(
            recommendations[:5],
            start=1
        ):

            content = recommendation["content"]

            with st.container(border=True):

                st.markdown(
                    f"### {index}. {content['title']}"
                )

                st.write(
                    content["description"]
                )

                st.caption(
                    f"Recommendation score: "
                    f"{recommendation['score']:.3f}"
                )


                # ----------------------------------
                # Explainability
                # ----------------------------------

                with st.expander(
                    "Why was this recommended?"
                ):

                    for reason in recommendation[
                        "explanation"
                    ]:

                        st.write(
                            f"• {reason}"
                        )


                # ----------------------------------
                # Feedback
                # ----------------------------------

                st.write(
                    "**Was this recommendation helpful?**"
                )

                feedback_col1, feedback_col2 = (
                    st.columns(2)
                )

                with feedback_col1:

                    if st.button(
                        "👍 Helpful",
                        key=(
                            f"helpful_"
                            f"{content['id']}"
                        )
                    ):

                        recommendation_engine.feedback.record_feedback(
                            recommendation_id=content["id"],
                            viewed=True,
                            accepted=True,
                            rejected=False
                        )

                        st.success(
                            "Thanks! Your feedback "
                            "was recorded."
                        )

                with feedback_col2:

                    if st.button(
                        "👎 Not Helpful",
                        key=(
                            f"not_helpful_"
                            f"{content['id']}"
                        )
                    ):

                        recommendation_engine.feedback.record_feedback(
                            recommendation_id=content["id"],
                            viewed=True,
                            accepted=False,
                            rejected=True
                        )

                        st.info(
                            "Thanks! Your feedback "
                            "was recorded."
                        )


                # ----------------------------------
                # Rating
                # ----------------------------------

                rating = st.selectbox(
                    "Rate this recommendation",
                    [1, 2, 3, 4, 5],
                    index=None,
                    placeholder=(
                        "Select a rating"
                    ),
                    key=(
                        f"rating_"
                        f"{content['id']}"
                    )
                )

                if rating is not None:

                    if st.button(
                        "Submit Rating",
                        key=(
                            f"submit_rating_"
                            f"{content['id']}"
                        )
                    ):

                        recommendation_engine.feedback.record_feedback(
                            recommendation_id=content["id"],
                            viewed=True,
                            rating=rating
                        )

                        st.success(
                            "Rating recorded."
                        )


    # ==================================================
    # Analysis Details
    # ==================================================

    with st.expander(
        "View Analysis Details"
    ):

        st.markdown(
            "**Original Text**"
        )

        st.write(
            result["text"]
        )

        st.markdown(
            "**Preprocessed Text**"
        )

        st.write(
            result["preprocessed_text"]
        )

        st.markdown(
            "**Primary Emotion**"
        )

        st.write(
            result["emotions"]["primary_emotion"]
        )


# ==================================================
# Session History
# ==================================================

st.markdown("---")

st.markdown("## 📜 Session History")

emotional_history = (
    history.get_emotional_history()
)

if not emotional_history:

    st.info(
        "No emotional analysis history yet."
    )

else:

    for record in reversed(
        emotional_history
    ):

        timestamp = record["timestamp"]

        state = (
            record["emotional_state"]
            ["emotional_state"]
        )

        intensity = (
            record["intensity"]
            ["severity"]
        )

        emotions = (
            record["emotions"]
            ["emotions"]
        )

        primary_emotion = (
            record["emotions"]
            ["primary_emotion"]
        )

        with st.container(border=True):

            st.write(
                f"**Time:** {timestamp}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"**State:** {state}"
                )

            with col2:

                st.write(
                    f"**Primary Emotion:** "
                    f"{primary_emotion}"
                )

            with col3:

                st.write(
                    f"**Intensity:** {intensity}"
                )

            st.write(
                "**Emotion Scores:** "
                + ", ".join(
                    f"{emotion}: {score:.2f}"
                    for emotion, score
                    in emotions.items()
                )
            )


# ==================================================
# Emotional Trend Analysis
# ==================================================

st.markdown("---")

st.markdown("## 📈 Emotional Trends")

emotional_history = (
    history.get_emotional_history()
)

if len(emotional_history) < 2:

    st.info(
        "Analyze at least two moods to view "
        "emotional trends."
    )

else:

    trend_data = (
        analyze_emotional_trends(
            emotional_history
        )
    )

    # ----------------------------------------------
    # Trend Summary
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Analyses",
            trend_data["total_analyses"]
        )

    with col2:

        dominant = (
            trend_data["dominant_emotion"]
        )

        st.metric(
            "Dominant Emotion",
            dominant.capitalize()
            if dominant
            else "N/A"
        )

    with col3:

        emotion_count = len(
            trend_data["emotion_frequency"]
        )

        st.metric(
            "Emotions Detected",
            emotion_count
        )


    # ----------------------------------------------
    # Emotion Frequency
    # ----------------------------------------------

    st.markdown(
        "### Emotion Frequency"
    )

    frequency = (
        trend_data["emotion_frequency"]
    )

    if frequency:

        st.bar_chart(
            frequency
        )


    # ----------------------------------------------
    # Average Intensity
    # ----------------------------------------------

    st.markdown(
        "### Average Emotional Intensity"
    )

    average_intensity = (
        trend_data["average_intensity"]
    )

    if average_intensity:

        st.bar_chart(
            average_intensity
        )


    # ----------------------------------------------
    # Trend Direction
    # ----------------------------------------------

    st.markdown(
        "### Trend Direction"
    )

    trend_direction = (
        trend_data["trend_direction"]
    )

    for emotion, direction in sorted(
        trend_direction.items()
    ):

        if direction == "Increasing":

            icon = "📈"

        elif direction == "Decreasing":

            icon = "📉"

        elif direction == "Stable":

            icon = "➡️"

        else:

            icon = "⚪"

        st.write(
            f"{icon} **{emotion.capitalize()}** "
            f"— {direction}"
        )


# ==================================================
# Recommendation History
# ==================================================

st.markdown("---")

st.markdown(
    "## 📝 Recommendation History"
)
recommendation_history = (
    history.get_recommendation_history()
)

if not recommendation_history:

    st.info(
        "No recommendation feedback has "
        "been recorded yet."
    )

else:

    # ==================================================
    # Search and Filters
    # ==================================================

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        search_text = st.text_input(
            "🔎 Search recommendation",
            placeholder="e.g. breathing_01"
        )

    with filter_col2:

        feedback_filter = st.selectbox(
            "Feedback",
            [
                "All",
                "Helpful",
                "Not Helpful",
                "No Feedback"
            ]
        )

    with filter_col3:

        rating_filter = st.selectbox(
            "Rating",
            [
                "All",
                "1 ⭐",
                "2 ⭐",
                "3 ⭐",
                "4 ⭐",
                "5 ⭐"
            ]
        )

    viewed_filter = st.selectbox(
        "Viewed",
        [
            "All",
            "Viewed",
            "Not Viewed"
        ]
    )

    # ==================================================
    # Apply Filters
    # ==================================================

    filtered_history = []

    for record in recommendation_history:

        recommendation_id = (
            record["recommendation_id"]
        )

        viewed = record["viewed"]
        accepted = record["accepted"]
        rejected = record["rejected"]
        rating = record["rating"]

        # Search filter
        if (
            search_text.strip()
            and search_text.lower()
            not in recommendation_id.lower()
        ):
            continue

        # Feedback filter
        if feedback_filter == "Helpful":
            if accepted is not True:
                continue

        elif feedback_filter == "Not Helpful":
            if rejected is not True:
                continue

        elif feedback_filter == "No Feedback":
            if accepted is not None or rejected:
                continue

        # Rating filter
        if rating_filter != "All":

            selected_rating = int(
                rating_filter[0]
            )

            if rating != selected_rating:
                continue

        # Viewed filter
        if viewed_filter == "Viewed":
            if viewed is not True:
                continue

        elif viewed_filter == "Not Viewed":
            if viewed is not False:
                continue

        filtered_history.append(record)

    # ==================================================
    # Filter Summary
    # ==================================================

    st.caption(
        f"Showing {len(filtered_history)} "
        f"of {len(recommendation_history)} "
        f"recommendation records."
    )

    # ==================================================
    # Display Filtered History
    # ==================================================

    if not filtered_history:

        st.info(
            "No recommendation history matches "
            "the selected filters."
        )

    else:

        for record in reversed(
            filtered_history
        ):

            recommendation_id = (
                record["recommendation_id"]
            )

            viewed = record["viewed"]
            accepted = record["accepted"]
            rejected = record["rejected"]
            rating = record["rating"]
            timestamp = record["timestamp"]

            with st.container(border=True):

                st.write(
                    f"**Recommendation:** "
                    f"`{recommendation_id}`"
                )

                st.write(
                    f"**Time:** {timestamp}"
                )

                if accepted is True:

                    st.write(
                        "**Feedback:** 👍 Helpful"
                    )

                elif rejected is True:

                    st.write(
                        "**Feedback:** 👎 Not Helpful"
                    )

                else:

                    st.write(
                        "**Feedback:** "
                        "No decision recorded"
                    )

                if rating is not None:

                    st.write(
                        f"**Rating:** "
                        f"{'⭐' * rating} "
                        f"({rating}/5)"
                    )

                st.write(
                    f"**Viewed:** "
                    f"{'Yes' if viewed else 'No'}"
                )

# ==================================================
# Report Generation and Export
# ==================================================

st.markdown("---")
st.header("📄 Report Generation & Export")

emotional_history = history.get_emotional_history()
recommendation_history = history.get_recommendation_history()

if not emotional_history:
    st.info(
        "Complete an emotional analysis to generate "
        "your wellness report."
    )
else:
    report_trend_data = analyze_emotional_trends(
        emotional_history
    )

    wellness_report = generate_wellness_report(
        emotional_history=emotional_history,
        recommendation_history=recommendation_history,
        trend_data=report_trend_data
    )

    st.download_button(
        label="📥 Download Wellness Report",
        data=wellness_report,
        file_name="mood_mentor_wellness_report.md",
        mime="text/markdown",
        key="download_wellness_report"
    )

    recommendation_csv = generate_recommendation_csv(
        recommendation_history
    )

    st.download_button(
        label="📊 Download Recommendation History (CSV)",
        data=recommendation_csv,
        file_name="mood_mentor_recommendation_history.csv",
        mime="text/csv",
        key="download_recommendation_history"
    )

    st.caption(
        "The wellness report excludes original mood text. "
        "The CSV contains recommendation interactions and feedback."
    )
