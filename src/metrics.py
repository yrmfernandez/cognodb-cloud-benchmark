import time
import statistics


def measure_workload(workload, adapter, iterations=30):
    """
    Execute a workload repeatedly and measure latency in milliseconds.
    """

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

        latency_ms = (end - start) * 1000
        latencies.append(latency_ms)

    return {
        "iterations": iterations,
        "successful": successful,
        "failed": failed,
        "average_ms": statistics.mean(latencies),
        "median_ms": statistics.median(latencies),
        "min_ms": min(latencies),
        "max_ms": max(latencies),
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