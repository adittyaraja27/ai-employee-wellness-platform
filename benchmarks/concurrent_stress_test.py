from threading import Lock
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from integration.mood_mentor_pipeline import MoodMentorPipeline
pipeline = MoodMentorPipeline()
inference_lock = Lock()

OUTPUT_FILE = Path("reports/concurrent_stress_test.json")
REQUESTS_PER_LEVEL = 30
CONCURRENCY_LEVELS = [2, 4, 8]

SAMPLES = [
    "I feel happy and motivated today.",
    "I am stressed about work but trying to stay positive.",
    (
        "I have many responsibilities and sometimes feel overwhelmed. "
        "I am trying to improve my routine and manage my stress."
    ),
]


def percentile(values, fraction):
    ordered = sorted(values)
    index = round((len(ordered) - 1) * fraction)
    return ordered[index]


def main():
    print("Mood Mentor Concurrent Stress Test")
    print("=" * 45)
    print("Loading one shared pipeline...")
    pipeline = MoodMentorPipeline()

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "requests_per_level": REQUESTS_PER_LEVEL,
        "shared_pipeline_instance": True,
        "results": {},
    }

    for workers in CONCURRENCY_LEVELS:
        print(f"\nTesting {workers} concurrent workers...")

        latencies = []
        errors = []
        completed = 0

        jobs = [
            SAMPLES[index % len(SAMPLES)]
            for index in range(REQUESTS_PER_LEVEL)
        ]

        def analyze_one(text):
            start = time.perf_counter()
        
            with inference_lock:
                result = pipeline.analyze(text)
        
            elapsed = time.perf_counter() - start
        
            if not result.get("emotions", {}).get("primary_emotion"):
                raise RuntimeError("Missing primary emotion")
        
            return elapsed

        wall_start = time.perf_counter()

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(analyze_one, text): index
                for index, text in enumerate(jobs)
            }

            for future in as_completed(futures):
                try:
                    latencies.append(future.result())
                    completed += 1
                except Exception as exc:
                    errors.append({
                        "request": futures[future] + 1,
                        "error": f"{type(exc).__name__}: {exc}",
                    })

        wall_seconds = time.perf_counter() - wall_start

        result = {
            "workers": workers,
            "requested": REQUESTS_PER_LEVEL,
            "successful": completed,
            "failed": len(errors),
            "wall_seconds": round(wall_seconds, 4),
            "throughput_requests_per_second": round(
                completed / wall_seconds, 2
            ) if wall_seconds else 0,
            "latency_seconds": {
                "mean": statistics.mean(latencies) if latencies else None,
                "median": statistics.median(latencies) if latencies else None,
                "p95": percentile(latencies, 0.95) if latencies else None,
                "max": max(latencies) if latencies else None,
            },
            "errors": errors,
        }

        report["results"][str(workers)] = result

        print(
            f"Success: {completed}/{REQUESTS_PER_LEVEL} | "
            f"Errors: {len(errors)} | "
            f"Throughput: "
            f"{result['throughput_requests_per_second']} requests/s"
        )

        if latencies:
            print(
                f"Median latency: "
                f"{result['latency_seconds']['median']:.4f}s | "
                f"P95: {result['latency_seconds']['p95']:.4f}s"
            )

        if errors:
            print("First error:", errors[0])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(report, indent=2))

    print("\n" + "=" * 45)
    print(f"Report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
