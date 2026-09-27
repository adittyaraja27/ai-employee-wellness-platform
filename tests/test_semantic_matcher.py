from recommendation.semantic_matcher import SemanticMatcher


matcher = SemanticMatcher()


text = "I'm extremely anxious about my upcoming presentation."

results = matcher.calculate_similarity(text)


print("\nSemantic Matching Results\n")

for item in results:

    print(
        f"{item['content']['title']} "
        f"→ Similarity: {item['similarity']:.4f}"
    )