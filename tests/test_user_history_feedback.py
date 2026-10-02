from user.history import UserHistory


def test_recommendation_feedback_history():

    history = UserHistory()

    # Record accepted recommendation
    history.add_recommendation_record(
        recommendation_id="walk_01",
        viewed=True,
        accepted=True,
        rejected=False,
        rating=5
    )

    # Record rejected recommendation
    history.add_recommendation_record(
        recommendation_id="break_01",
        viewed=True,
        accepted=False,
        rejected=True,
        rating=2
    )

    # Retrieve recommendation history
    records = history.get_recommendation_history()

    print("\nUser History Feedback Test")
    print("--------------------------")

    print("Total records:", len(records))

    for record in records:
        print("\nRecommendation:", record["recommendation_id"])
        print("Viewed:", record["viewed"])
        print("Accepted:", record["accepted"])
        print("Rejected:", record["rejected"])
        print("Rating:", record["rating"])
        print("Timestamp:", record["timestamp"])

    # Verify records
    assert len(records) == 2

    assert records[0]["recommendation_id"] == "walk_01"
    assert records[0]["accepted"] is True
    assert records[0]["rating"] == 5

    assert records[1]["recommendation_id"] == "break_01"
    assert records[1]["rejected"] is True
    assert records[1]["rating"] == 2

    print("\nUSER HISTORY FEEDBACK TEST PASSED")


if __name__ == "__main__":
    test_recommendation_feedback_history()