
import gc
import json
import resource
import statistics
import time
from datetime import datetime
from pathlib import Path

from integration.mood_mentor_pipeline import MoodMentorPipeline


OUTPUT_FILE = Path("reports/stress_test.json")
TOTAL_RUNS = 50

SAMPLES = [
    "I feel happy and motivated today.",
    (
        "I am feeling stressed about my workload, "
        "but I am trying to stay calm and focused."
    ),
    (
        "Over the past few weeks, I have had several "
        "responsibilities at work and at home. I sometimes "
        "feel overwhelmed by deadlines, but I am trying to "
        "improve my routine, communicate better, and maintain "
        "a positive outlook while managing these challenges."
    ),
]


def percentile(values, fraction):
    ordered = sorted(values)
    index = round((len(ordered) - 1) * fraction)
    return ordered[index]


def main():
    print("Mood Mentor Repeated-Request Stress Test")
    print("=" * 45)

    pipeline = MoodMentorPipeline()

    # Establish a baseline for repeated identical input.
    baseline = pipeline.analyze(SAMPLES[0])
    expected_emotion = baseline["emotions"]["primary_emotion"]
    expected_state = baseline["emotional_state"]["emotional_state"]

    latencies = []
    errors = []
    consistent_results = 0

    gc.collect()
    start_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    for index in range(TOTAL_RUNS):
        text = SAMPLES[index % len(SAMPLES)]

        start = time.perf_counter()

        try:
            result = pipeline.analyze(text)
            elapsed = time.perf_counter() - start
            latencies.append(elapsed)

            if not result.get("emotions", {}).get("primary_emotion"):
                errors.append(f"Run {index + 1}: missing primary emotion")
                continue

            if text == SAMPLES[0]:
                if (
                    result["emotions"]["primary_emotion"] == expected_emotion
                    and result["emotional_state"]["emotional_state"]
                    == expected_state
                ):
                    consistent_results += 1

        except Exception as exc:
            errors.append(f"Run {index + 1}: {type(exc).__name__}: {exc}")

        if (index + 1) % 10 == 0:
            print(f"Completed {index + 1}/{TOTAL_RUNS} requests")

    end_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # Verify invalid inputs are rejected as expected.
    invalid_inputs = ["", "   ", "\n\t"]
    invalid_input_checks = []

    for text in invalid_inputs:
        try:
            pipeline.analyze(text)
            invalid_input_checks.append({
                "input": repr(text),
                "rejected": False,
            })
        except ValueError:
            invalid_input_checks.append({
                "input": repr(text),
                "rejected": True,
            })
        except Exception as exc:
            invalid_input_checks.append({
                "input": repr(text),
                "rejected": False,
                "unexpected_error": type(exc).__name__,
            })

    success_count = len(latencies) - len(errors)

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_requests": TOTAL_RUNS,
        "successful_requests": success_count,
        "errors": errors,
        "latency_seconds": {
            "mean": statistics.mean(latencies) if latencies else None,
            "median": statistics.median(latencies) if latencies else None,
            "p95": percentile(latencies, 0.95) if latencies else None,
            "max": max(latencies) if latencies else None,
        },
        "same_input_consistency": {
            "expected_primary_emotion": expected_emotion,
            "expected_emotional_state": expected_state,
            "matching_results": consistent_results,
            "total_comparisons": sum(
                1 for i in range(TOTAL_RUNS) if SAMPLES[i % len(SAMPLES)] == SAMPLES[0]
            ),
        },
        "invalid_input_checks": invalid_input_checks,
        "peak_process_rss_mb": round(end_rss / (1024 * 1024), 2),
        "initial_process_peak_rss_mb": round(start_rss / (1024 * 1024), 2),
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(report, indent=2))

    print("\nResults")
    print("-" * 45)
    print(f"Successful requests: {success_count}/{TOTAL_RUNS}")
    print(f"Errors: {len(errors)}")

    if latencies:
        print(f"Mean latency: {statistics.mean(latencies):.4f}s")
        print(f"Median latency: {statistics.median(latencies):.4f}s")
        print(f"P95 latency: {percentile(latencies, 0.95):.4f}s")
        print(f"Maximum latency: {max(latencies):.4f}s")

    print(f"Repeated-input matches: {consistent_results}")
    print(f"Peak process RSS: {report['peak_process_rss_mb']} MB")
    print(f"Report saved to: {OUTPUT_FILE}")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(error)

    if not all(item["rejected"] for item in invalid_input_checks):
        print("\nWARNING: At least one invalid-input check failed.")

    if errors or success_count != TOTAL_RUNS:
        raise SystemExit("Stress test failed: inspect the report and errors.")

    if not all(item["rejected"] for item in invalid_input_checks):
        raise SystemExit("Stress test failed: invalid input was not rejected.")

    if consistent_results != report["same_input_consistency"]["total_comparisons"]:
        raise SystemExit("Stress test failed: repeated input results differed.")


if __name__ == "__main__":
    main()
