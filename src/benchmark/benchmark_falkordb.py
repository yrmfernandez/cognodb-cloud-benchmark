import os
import time
import statistics
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv

from adapters.falkordb import FalkordbAdapter


ITERATIONS = 30
TEST_USER_ID = 30


def percentile(values, percentile):
    values = sorted(values)

    index = (percentile / 100) * (len(values) - 1)
    lower = int(index)
    upper = min(lower + 1, len(values))

    if lower == upper:
        return values[lower]

    return values[lower] + (values[upper] - values[lower]) * (index - lower)


def main():
    load_dotenv()

    adapter = FalkordbAdapter()

    print("Connecting to Falkordb...")
    adapter.connect()
    print("Connected successfully.\n")

    print("Running Point Lookup benchmark...")
    print(f"Iterations: {ITERATIONS}\n")

    times = []
    successful = 0
    failed = 0

    try:
        for _ in range(ITERATIONS):
            start = time.perf_counter()

            try:
                result = adapter.point_lookup(TEST_USER_ID)

                elapsed = (time.perf_counter() - start) * 1000

                if result is not None:
                    successful += 1
                    times.append(elapsed)
                else:
                    failed += 1

            except Exception as e:
                failed += 1
                print(f"Benchmark iteration failed: {e}")

    finally:
        adapter.close()

    if not times:
        print("No successful benchmark iterations.")
        return

    average = statistics.mean(times)
    median = statistics.median(times)
    minimum = min(times)
    maximum = max(times)
    p95 = percentile(times, 95)

    print("Benchmark Results")
    print("-----------------")
    print(f"Iterations: {ITERATIONS}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Average: {average:.3f} ms")
    print(f"Median:  {median:.3f} ms")
    print(f"Minimum: {minimum:.3f} ms")
    print(f"Maximum: {maximum:.3f} ms")
    print(f"P95:     {p95:.3f} ms")


if __name__ == "__main__":
    main()