class UserProfile:

    def __init__(self, user_id):
        if not user_id:
            raise ValueError("User ID cannot be empty")

        self.user_id = user_id

        self.preferences = {
            "activities": [],
            "content_types": [],
            "interests": []
        }

        self.preference_history = []

    def update_preferences(
        self,
        activities=None,
        content_types=None,
        interests=None
    ):
        """
        Update the user's preferences.

        Only supplied values are updated.
        """

        old_preferences = self.preferences.copy()

        if activities is not None:
            self.preferences["activities"] = activities

        if content_types is not None:
            self.preferences["content_types"] = content_types

        if interests is not None:
            self.preferences["interests"] = interests

        # Store the change for future feedback analysis
        self.preference_history.append({
            "old_preferences": old_preferences,
            "new_preferences": self.preferences.copy()
        })

    def get_preferences(self):
        return self.preferences.copy()

    def get_preference_history(self):
        return self.preference_history.copy()