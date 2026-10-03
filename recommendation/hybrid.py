from recommendation.content import WELLNESS_CONTENT
from recommendation.semantic_matcher import SemanticMatcher
from recommendation.feedback import RecommendationFeedback
from recommendation.explainability import generate_explanation

SEMANTIC_WEIGHT = 3
FEEDBACK_WEIGHT = 1


class HybridRecommendationEngine:

    def __init__(self, history=None):
        self.semantic_matcher = SemanticMatcher()
        self.feedback = RecommendationFeedback(history)

    def calculate_score(
        self,
        content,
        primary_emotion,
        intensity,
        user_preferences,
        semantic_similarity,
        feedback_score
    ):
        emotion_score = 0
        intensity_score = 0
        preference_score = 0

        # 1. Emotion relevance
        if primary_emotion in content["emotions"]:
            emotion_score = 4

        # 2. Intensity relevance
        if intensity in content["intensity"]:
            intensity_score = 3

        # 3. Activity preference
        if content["activity"] in user_preferences["activities"]:
            preference_score += 2

        # 4. Content type preference
        if content["content_type"] in user_preferences["content_types"]:
            preference_score += 2

        # 5. Semantic relevance
        semantic_score = semantic_similarity * SEMANTIC_WEIGHT
        feedback_adjustment = feedback_score * FEEDBACK_WEIGHT
        final_score = (
            emotion_score
            + intensity_score
            + preference_score
            + semantic_score
            + feedback_adjustment
)

        return {
            "emotion_score": emotion_score,
            "intensity_score": intensity_score,
            "preference_score": preference_score,
            "semantic_score": semantic_score,
            "feedback_score": feedback_adjustment,
            "final_score": final_score
        }

    def generate_recommendations(
        self,
        user_text,
        emotion_result,
        intensity_result,
        user_preferences=None
    ):

        if user_preferences is None:
            user_preferences = {
                "activities": [],
                "content_types": [],
                "interests": []
            }

        primary_emotion = emotion_result["primary_emotion"]
        intensity = intensity_result["severity"].lower()

        semantic_results = self.semantic_matcher.calculate_similarity(
            user_text
        )

        recommendations = []

        for item in semantic_results:

            content = item["content"]
            similarity = item["similarity"]
            feedback_score = self.feedback.calculate_feedback_score(
                content["id"]
            )
            score_breakdown = self.calculate_score(
                content,
                primary_emotion,
                intensity,
                user_preferences,
                similarity,
                feedback_score
            )

            if score_breakdown["final_score"] > 0:

                explanation = generate_explanation(
                    content=content,
                    primary_emotion=primary_emotion,
                    intensity=intensity,
                    score_breakdown=score_breakdown
                )
                
                recommendations.append({
                    "content": content,
                    "score": round(
                        score_breakdown["final_score"],
                        4
                    ),
                    "semantic_similarity": round(
                        similarity,
                        4
                    ),
                    "score_breakdown": score_breakdown,
                    "explanation": explanation
                })

        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return recommendations