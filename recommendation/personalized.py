from recommendation.content import WELLNESS_CONTENT


def generate_recommendations(emotion_result, intensity_result, user_preferences=None):
    """
    Generate personalized wellness recommendations
    based on emotion, intensity, and user preferences.
    """

    primary_emotion = emotion_result["primary_emotion"]
    intensity = intensity_result["severity"].lower()

    if user_preferences is None:
        user_preferences = {
            "activities": [],
            "content_types": [],
            "interests": []
        }

    recommendations = []

    for content in WELLNESS_CONTENT:

        score = 0

        # Emotion match
        if primary_emotion in content["emotions"]:
            score += 3

        # Intensity match
        if intensity in content["intensity"]:
            score += 2

        # Activity preference
        if content["activity"] in user_preferences["activities"]:
            score += 2

        # Content type preference
        if content["content_type"] in user_preferences["content_types"]:
            score += 2

        if score > 0:
            recommendations.append({
                "content": content,
                "score": score
            })

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return recommendations