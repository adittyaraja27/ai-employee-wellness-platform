from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from recommendation.content import WELLNESS_CONTENT


MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticMatcher:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

        self.content_texts = [
            content["title"] + ". " + content["description"]
            for content in WELLNESS_CONTENT
        ]

        self.content_embeddings = self.model.encode(
            self.content_texts,
            normalize_embeddings=True
        )

    def calculate_similarity(self, user_text):
        user_embedding = self.model.encode(
            [user_text],
            normalize_embeddings=True
        )

        similarities = cosine_similarity(
            user_embedding,
            self.content_embeddings
        )[0]

        results = []

        for content, similarity in zip(
            WELLNESS_CONTENT,
            similarities
        ):
            results.append({
                "content": content,
                "similarity": float(similarity)
            })

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        return results