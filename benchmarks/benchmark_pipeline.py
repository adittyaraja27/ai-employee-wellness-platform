
import json
import platform
import statistics
import time
from datetime import datetime
from pathlib import Path

import torch

from integration.mood_mentor_pipeline import MoodMentorPipeline


OUTPUT_DIR = Path("reports")
OUTPUT_FILE = OUTPUT_DIR / "performance_benchmark.json"

SAMPLES = {
    "short": "I feel happy today.",
    "medium": (
        "I have been feeling stressed about work lately, "
        "but I am trying to stay positive and manage my responsibilities."
    ),
    "long": (
        "Over the past few weeks, I have been dealing with "
        "several responsibilities at work and at home. "
        "Sometimes I feel anxious and overwhelmed, especially "
        "when deadlines approach. However, I am trying to improve "
        "my routine, take breaks, communicate with my colleagues, "
        "and maintain a positive outlook while managing these challenges. "
    ) * 4,
}

WARMUP_RUNS = 2
BENCHMARK_RUNS = 10


def percentile(values, percent):
    ordered = sorted(values)
    index = round((len(ordered) - 1) * percent)
    return ordered[index]


def measure_latency(pipeline, text, runs):
    durations = []

    for _ in range(runs):
        start = time.perf_counter()
        result = pipeline.analyze(text)
        elapsed = time.perf_counter() - start

        if not result.get("emotions"):
            raise RuntimeError("Pipeline returned no emotion results")

        durations.append(elapsed)

    return {
        "runs": runs,
        "mean_seconds": statistics.mean(durations),
        "median_seconds": statistics.median(durations),
        "min_seconds": min(durations),
        "max_seconds": max(durations),
        "p95_seconds": percentile(durations, 0.95),
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Mood Mentor Performance Benchmark")
    print("=" * 40)
    print(f"Python: {platform.python_version()}")
    print(f"PyTorch: {torch.__version__}")
    print(f"MPS available: {torch.backends.mps.is_available()}")

    load_start = time.perf_counter()
    pipeline = MoodMentorPipeline()
    model_load_seconds = time.perf_counter() - load_start

    print(f"\nModel initialization: {model_load_seconds:.3f} seconds")

    results = {}

    for sample_name, text in SAMPLES.items():
        print(f"\nBenchmarking {sample_name} input...")

        # Warm-up helps reduce one-time initialization effects.
        for _ in range(WARMUP_RUNS):
            pipeline.analyze(text)

        results[sample_name] = measure_latency(
            pipeline,
            text,
            BENCHMARK_RUNS,
        )

        print(
            f"Median: {results[sample_name]['median_seconds']:.3f}s | "
            f"Mean: {results[sample_name]['mean_seconds']:.3f}s | "
            f"Max: {results[sample_name]['max_seconds']:.3f}s"
        )

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "pytorch_version": torch.__version__,
        "mps_available": torch.backends.mps.is_available(),
        "model_path": "models/bert",
        "model_initialization_seconds": model_load_seconds,
        "warmup_runs_per_input": WARMUP_RUNS,
        "benchmark_runs_per_input": BENCHMARK_RUNS,
        "results": results,
    }

    OUTPUT_FILE.write_text(json.dumps(report, indent=2))

    print("\n" + "=" * 40)
    print(f"Benchmark report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
