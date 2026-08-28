import time
import statistics


def measure_workload(workload, adapter, iterations=100, warmup_iterations=30):
    """
    Execute a workload repeatedly and measure latency in milliseconds.

    Warm-up iterations are executed first and are NOT included
    in the benchmark results.
    """

    # -------------------------
    # Warm-up phase
    # -------------------------
    for _ in range(warmup_iterations):
        try:
            workload(adapter)
        except Exception:
            pass

    # -------------------------
    # Measurement phase
    # -------------------------
    latencies = []
    successful = 0
    failed = 0

    for _ in range(iterations):
        start = time.perf_counter()

        try:
            workload(adapter)
            successful += 1
        except Exception:
            failed += 1

        end = time.perf_counter()

        latencies.append((end - start) * 1000)

    # -------------------------
    # Results
    # -------------------------
    return {
        "iterations": iterations,
        "warmup_iterations": warmup_iterations,
        "successful": successful,
        "failed": failed,
        "average_ms": statistics.mean(latencies),
        "median_ms": statistics.median(latencies),
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "p50_ms": percentile(latencies, 50),
        "p95_ms": percentile(latencies, 95),
    }


def percentile(values, percentile_value):
    """
    Calculate a percentile using linear interpolation.
    """

    values = sorted(values)

    if not values:
        return None

    if len(values) == 1:
        return values[0]

    position = (len(values) - 1) * (percentile_value / 100)

    lower = int(position)
    upper = lower + 1

    if upper >= len(values):
        return values[-1]

    fraction = position - lower

    return (
        values[lower]
        + (values[upper] - values[lower]) * fraction
    )