def generate_explanation(
    content,
    primary_emotion,
    intensity,
    score_breakdown
):
    reasons = []

    # Emotion relevance
    if score_breakdown["emotion_score"] > 0:
        reasons.append(
            f"Your dominant emotion is {primary_emotion}."
        )

    # Intensity relevance
    if score_breakdown["intensity_score"] > 0:
        reasons.append(
            f"This activity matches your current {intensity} emotional intensity."
        )

    # Preference relevance
    if score_breakdown["preference_score"] > 0:
        reasons.append(
            "This recommendation matches your preferences."
        )

    # Semantic relevance
    if score_breakdown["semantic_score"] > 0:
        reasons.append(
            "This recommendation is relevant to what you wrote."
        )

    # Feedback learning
    if score_breakdown["feedback_score"] > 0:
        reasons.append(
            "Your previous feedback helped increase the relevance of this recommendation."
        )

    if not reasons:
        reasons.append(
            "This recommendation was selected based on its overall relevance."
        )

    return reasons