from datetime import datetime


class UserHistory:

    def __init__(self):
        self.emotional_history = []
        self.recommendation_history = []
        self.interaction_history = []

    def add_emotional_record(
        self,
        emotions,
        intensity,
        emotional_state
    ):
        self.emotional_history.append({
            "timestamp": datetime.now().isoformat(),
            "emotions": emotions,
            "intensity": intensity,
            "emotional_state": emotional_state
        })

    def add_recommendation_record(
        self,
        recommendation_id,
        viewed=False,
        accepted=None,
        rejected=False,
        rating=None
    ):
        self.recommendation_history.append({
            "timestamp": datetime.now().isoformat(),
            "recommendation_id": recommendation_id,
            "viewed": viewed,
            "accepted": accepted,
            "rejected": rejected,
            "rating": rating
        })

    def add_interaction(self, interaction):
        self.interaction_history.append({
            "timestamp": datetime.now().isoformat(),
            "interaction": interaction
        })

    def get_emotional_history(self):
        return self.emotional_history.copy()

    def get_recommendation_history(self):
        return self.recommendation_history.copy()

    def get_interaction_history(self):
        return self.interaction_history.copy()