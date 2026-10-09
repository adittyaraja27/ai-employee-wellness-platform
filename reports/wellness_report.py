from datetime import datetime
import csv
import io


def generate_wellness_report(
    emotional_history,
    recommendation_history,
    trend_data
):
    """
    Generate a complete Mood Mentor wellness report.

    The report summarizes emotional analysis, trends,
    recommendation activity, feedback, and ratings.
    """

    if not emotional_history:
        raise ValueError("No emotional history available for report")

    lines = []

    lines.append("# Mood Mentor Wellness Report")
    lines.append("")
    lines.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    lines.append("")

    # Emotional analysis summary
    lines.append("## Emotional Analysis")
    lines.append("")

    total_analyses = trend_data.get("total_analyses", 0)
    dominant_emotion = trend_data.get("dominant_emotion")

    lines.append(f"- Total analyses: {total_analyses}")
    lines.append(
        f"- Dominant emotion: "
        f"{dominant_emotion.capitalize() if dominant_emotion else 'N/A'}"
    )
    lines.append("")

    # Emotion frequency
    lines.append("## Emotion Frequency")
    lines.append("")

    emotion_frequency = trend_data.get(
        "emotion_frequency",
        {}
    )

    if emotion_frequency:
        for emotion, count in sorted(
            emotion_frequency.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            lines.append(
                f"- {emotion.capitalize()}: {count}"
            )
    else:
        lines.append("- No emotion frequency data available.")

    lines.append("")

    # Average intensity
    lines.append("## Average Emotional Intensity")
    lines.append("")

    average_intensity = trend_data.get(
        "average_intensity",
        {}
    )

    if average_intensity:
        for emotion, intensity in average_intensity.items():
            lines.append(
                f"- {emotion.capitalize()}: {intensity:.2f}"
            )
    else:
        lines.append("- No intensity data available.")

    lines.append("")

    # Trends
    lines.append("## Emotional Trends")
    lines.append("")

    trend_direction = trend_data.get(
        "trend_direction",
        {}
    )

    if trend_direction:
        for emotion, direction in trend_direction.items():
            lines.append(
                f"- {emotion.capitalize()}: {direction}"
            )
    else:
        lines.append("- No trend data available.")

    lines.append("")

    # Recommendation summary
    lines.append("## Recommendation Summary")
    lines.append("")

    total_recommendations = len(recommendation_history)

    helpful = sum(
        1
        for record in recommendation_history
        if record["accepted"] is True
    )

    not_helpful = sum(
        1
        for record in recommendation_history
        if record["rejected"] is True
    )

    ratings = [
        record["rating"]
        for record in recommendation_history
        if record["rating"] is not None
    ]

    lines.append(
        f"- Recommendation interactions: {total_recommendations}"
    )
    lines.append(f"- Helpful feedback: {helpful}")
    lines.append(f"- Not helpful feedback: {not_helpful}")

    if helpful + not_helpful > 0:
        acceptance_rate = helpful / (helpful + not_helpful)
        lines.append(
            f"- Acceptance rate: {acceptance_rate:.1%}"
        )
    else:
        lines.append("- Acceptance rate: N/A")

    if ratings:
        average_rating = sum(ratings) / len(ratings)
        lines.append(
            f"- Average rating: {average_rating:.2f}/5"
        )
    else:
        lines.append("- Average rating: N/A")

    lines.append("")

    # Recommendation history
    lines.append("## Recommendation History")
    lines.append("")

    if recommendation_history:
        for record in recommendation_history:
            recommendation_id = record["recommendation_id"]
            viewed = record["viewed"]
            accepted = record["accepted"]
            rejected = record["rejected"]
            rating = record["rating"]

            if accepted is True:
                feedback = "Helpful"
            elif rejected is True:
                feedback = "Not Helpful"
            else:
                feedback = "No Feedback"

            rating_text = (
                f"{rating}/5"
                if rating is not None
                else "N/A"
            )

            lines.append(
                f"- **{recommendation_id}** | "
                f"Viewed: {viewed} | "
                f"Feedback: {feedback} | "
                f"Rating: {rating_text}"
            )
    else:
        lines.append("- No recommendation history available.")

    lines.append("")

    lines.append("## Privacy Note")
    lines.append("")
    lines.append(
        "This report contains aggregated wellness analysis, "
        "trend information, and recommendation feedback. "
        "Original user-entered mood text is not included."
    )

    return "\n".join(lines)


def generate_recommendation_csv(recommendation_history):
    """
    Generate a CSV export of recommendation history.
    """

    output = io.StringIO()

    fieldnames = [
        "timestamp",
        "recommendation_id",
        "viewed",
        "accepted",
        "rejected",
        "rating"
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for record in recommendation_history:
        writer.writerow({
            "timestamp": record.get("timestamp", ""),
            "recommendation_id": record.get(
                "recommendation_id",
                ""
            ),
            "viewed": record.get("viewed", ""),
            "accepted": record.get("accepted", ""),
            "rejected": record.get("rejected", ""),
            "rating": record.get("rating", "")
        })

    return output.getvalue()
