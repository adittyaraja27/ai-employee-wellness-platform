from recommendation.content import WELLNESS_CONTENT


def hybrid_score(
    content,
    primary_emotion,
    intensity,
    user_preferences
):
    score = 0

    # 1. Emotion relevance
    if primary_emotion in content["emotions"]:
        score += 4

    # 2. Intensity relevance
    if intensity in content["intensity"]:
        score += 3

    # 3. Activity preference
    if content["activity"] in user_preferences["activities"]:
        score += 2

    # 4. Content type preference
    if content["content_type"] in user_preferences["content_types"]:
        score += 2

    return score


def generate_hybrid_recommendations(
    emotion_result,
    intensity_result,
    user_preferences=None
):
    if user_preferences is None:
        user_preferences = {
            "activities": ["walking"],
            "content_types": [],
            "interests": []
        }

        recommendations = generate_hybrid_recommendations(
            emotion_result,
            intensity_result,
            user_preferences
        )

    primary_emotion = emotion_result["primary_emotion"]
    intensity = intensity_result["severity"].lower()

    recommendations = []

    for content in WELLNESS_CONTENT:

        score = hybrid_score(
            content,
            primary_emotion,
            intensity,
            user_preferences
        )

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