from user.history import UserHistory
class RecommendationFeedback:

    def __init__(self, history=None):
        self.history = history

        if history is None:
            self.feedback_history = []
    def record_feedback(
        self,
        recommendation_id,
        viewed=False,
        accepted=None,
        rejected=False,
        rating=None
    ):  
        if self.history is not None:
            self.history.add_recommendation_record(
                recommendation_id=recommendation_id,
                viewed=viewed,
                accepted=accepted,
                rejected=rejected,
                rating=rating
            )
            return

        feedback = {
            "recommendation_id": recommendation_id,
            "viewed": viewed,
            "accepted": accepted,
            "rejected": rejected,
            "rating": rating
        }

        self.feedback_history.append(feedback)

    def get_feedback_history(self):

        if self.history is not None:
            return self.history.get_recommendation_history()

        return self.feedback_history.copy()

    def get_recommendation_feedback(self, recommendation_id):

        feedback_history = self.get_feedback_history()
    
        return [
            feedback
            for feedback in feedback_history
            if feedback["recommendation_id"] == recommendation_id
        ]

    def calculate_acceptance_rate(self, recommendation_id):
        feedback = self.get_recommendation_feedback(
            recommendation_id
        )

        decisions = [
            item
            for item in feedback
            if item["accepted"] is not None
        ]

        if not decisions:
            return 0.0

        accepted = sum(
            1
            for item in decisions
            if item["accepted"] is True
        )

        return accepted / len(decisions)

    def calculate_average_rating(self, recommendation_id):
        feedback = self.get_recommendation_feedback(
            recommendation_id
        )

        ratings = [
            item["rating"]
            for item in feedback
            if item["rating"] is not None
        ]

        if not ratings:
            return 0.0

        return sum(ratings) / len(ratings)

    def calculate_feedback_score(self, recommendation_id):
        feedback = self.get_recommendation_feedback(
            recommendation_id
        )

        if not feedback:
            return 0.0

        acceptance_rate = self.calculate_acceptance_rate(
            recommendation_id
        )

        average_rating = self.calculate_average_rating(
            recommendation_id
        )

        # Acceptance contribution
        acceptance_score = (acceptance_rate - 0.5) * 2

        # Rating contribution
        if average_rating > 0:
            rating_score = (average_rating - 3) / 2
        else:
            rating_score = 0.0

        # Combine both signals
        feedback_score = (
            acceptance_score * 0.6
            + rating_score * 0.4
        )

        # Keep feedback influence limited
        return round(feedback_score, 4)