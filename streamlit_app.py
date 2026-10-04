import streamlit as st

from integration.mood_mentor_pipeline import MoodMentorPipeline
from user.history import UserHistory
from recommendation.hybrid import HybridRecommendationEngine


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Mood Mentor",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# Initialize application components
# --------------------------------------------------

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


# --------------------------------------------------
# Page header
# --------------------------------------------------

st.title("🧠 Mood Mentor")
st.subheader("AI-Based Employee Wellness Management Platform")

st.write(
    "Describe how you are feeling, and Mood Mentor will analyze "
    "your emotional state and provide personalized wellness recommendations."
)


# --------------------------------------------------
# Mood input
# --------------------------------------------------

st.markdown("### How are you feeling?")

user_text = st.text_area(
    "Write about your current thoughts or feelings:",
    placeholder="Example: I have been feeling stressed about my workload today...",
    height=150
)


# --------------------------------------------------
# Analyze button
# --------------------------------------------------

if st.button("Analyze My Mood", type="primary"):

    if not user_text.strip():
        st.warning("Please enter some text before analyzing.")
        st.stop()

    try:
        # ------------------------------------------
        # AI analysis
        # ------------------------------------------

        with st.spinner("Analyzing your emotional state..."):
            result = pipeline.analyze(user_text)

        # ------------------------------------------
        # Store emotional history
        # ------------------------------------------

        history.add_emotional_record(
            emotions=result["emotions"],
            intensity=result["intensity"],
            emotional_state=result["emotional_state"]
        )

        # ------------------------------------------
        # Generate recommendations
        # ------------------------------------------

        recommendations = recommendation_engine.generate_recommendations(
            user_text=user_text,
            emotion_result=result["emotions"],
            intensity_result=result["intensity"]
        )

        # ------------------------------------------
        # Analysis results
        # ------------------------------------------

        st.success("Analysis completed successfully.")

        st.markdown("## 📊 Emotional Analysis")

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

        # ------------------------------------------
        # Emotion scores
        # ------------------------------------------

        st.markdown("### Emotion Scores")

        emotions = result["emotions"]["emotions"]

        for emotion, score in emotions.items():
            st.write(
                f"**{emotion.capitalize()}** — {score:.3f}"
            )
            st.progress(float(score))

        # ------------------------------------------
        # Recommendations
        # ------------------------------------------

        st.markdown("## 💡 Personalized Recommendations")

        if not recommendations:
            st.info("No recommendations were generated.")
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

                    st.write(content["description"])

                    st.caption(
                        f"Recommendation score: "
                        f"{recommendation['score']:.3f}"
                    )

                    with st.expander("Why was this recommended?"):

                        for reason in recommendation["explanation"]:
                            st.write(f"• {reason}")

        # ------------------------------------------
        # Analysis details
        # ------------------------------------------

        with st.expander("View Analysis Details"):

            st.markdown("**Original Text**")
            st.write(result["text"])

            st.markdown("**Preprocessed Text**")
            st.write(result["preprocessed_text"])

            st.markdown("**Primary Emotion**")
            st.write(result["emotions"]["primary_emotion"])

    except Exception as e:

        st.error("An error occurred during analysis.")

        with st.expander("Technical Details"):
            st.code(str(e))


# --------------------------------------------------
# User history
# --------------------------------------------------

st.markdown("---")

st.markdown("## 📜 Session History")

emotional_history = history.get_emotional_history()

if not emotional_history:
    st.info("No emotional analysis history yet.")
else:

    for record in reversed(emotional_history):

        timestamp = record["timestamp"]

        state = record["emotional_state"]["emotional_state"]

        intensity = record["intensity"]["severity"]

        emotions = record["emotions"]["emotions"]

        primary_emotion = record["emotions"]["primary_emotion"]

        with st.container(border=True):

            st.write(f"**Time:** {timestamp}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**State:** {state}")

            with col2:
                st.write(f"**Primary Emotion:** {primary_emotion}")

            with col3:
                st.write(f"**Intensity:** {intensity}")

            st.write(
                "**Emotion Scores:** "
                + ", ".join(
                    f"{emotion}: {score:.2f}"
                    for emotion, score in emotions.items()
                )
            )
# --------------------------------------------------
# Emotional Trend Analysis
# --------------------------------------------------

from recommendation.trend_analyzer import analyze_emotional_trends


st.markdown("---")

st.markdown("## 📈 Emotional Trends")

emotional_history = history.get_emotional_history()

if len(emotional_history) < 2:

    st.info(
        "Analyze at least two moods to view emotional trends."
    )

else:

    trend_data = analyze_emotional_trends(
        emotional_history
    )

    # ----------------------------------------------
    # Trend summary
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Analyses",
            trend_data["total_analyses"]
        )

    with col2:
        dominant = trend_data["dominant_emotion"]

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
    # Emotion frequency
    # ----------------------------------------------

    st.markdown("### Emotion Frequency")

    frequency = trend_data["emotion_frequency"]

    if frequency:

        st.bar_chart(frequency)

    # ----------------------------------------------
    # Average intensity
    # ----------------------------------------------

    st.markdown("### Average Emotional Intensity")

    average_intensity = trend_data["average_intensity"]

    if average_intensity:

        st.bar_chart(average_intensity)

    # ----------------------------------------------
    # Trend direction
    # ----------------------------------------------

    st.markdown("### Trend Direction")

    trend_direction = trend_data["trend_direction"]

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
            f"{icon} **{emotion.capitalize()}** — {direction}"
        )
