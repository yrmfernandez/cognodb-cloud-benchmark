import json
import os

from adapters.cognodb import CognoDBAdapter
from adapters.neo4j import Neo4jAdapter
from adapters.memgraph import MemgraphAdapter
from adapters.arangodb import ArangodbAdapter
from adapters.falkordb import FalkordbAdapter

from workloads import (
    point_lookup,
    hop_1,
    hop_2,
    hop_3,
    indexed_lookup,
    aggregation,
)
from metrics import measure_workload

ITERATIONS = 100
WARMUP_ITERATIONS = 30
USER_ID = 30
RESULTS_DIR = "results"

DATABASES = [
    ("cognodb", CognoDBAdapter),
    ("neo4j", Neo4jAdapter),
    ("memgraph", MemgraphAdapter),
    ("arangodb", ArangodbAdapter),
    ("falkordb", FalkordbAdapter),
]

# Workloads to run against every database. Add more entries here as
# workloads.py grows (e.g. hop_1, aggregation) -- nothing else in this
# file needs to change.
WORKLOADS = {
    "point_lookup": lambda adapter: point_lookup(adapter, user_id=USER_ID),
    "hop_1": lambda adapter: hop_1(adapter, user_id=USER_ID),
    "hop_2": lambda adapter: hop_2(adapter, user_id=USER_ID),
    "hop_3": lambda adapter: hop_3(adapter, user_id=USER_ID),
    "indexed_lookup": lambda adapter: indexed_lookup(adapter, user_type=0),
    "aggregation": aggregation,
}


def run_database(db_name, adapter_cls):
    print(f"\n{'=' * 50}")
    print(f"Benchmarking {db_name}")
    print("=" * 50)

    adapter = adapter_cls()
    db_results = {"database": db_name}
    error = None

    try:
        print(f"Connecting to {db_name}...")
        adapter.connect()
        print("Connected successfully.")

        for workload_name, workload_fn in WORKLOADS.items():
            print(f"\nRunning {workload_name} benchmark...")
            print(f"Iterations: {ITERATIONS}")

            results = measure_workload(
                workload=workload_fn,
                adapter=adapter,
                iterations=ITERATIONS,
                warmup_iterations=WARMUP_ITERATIONS,
            )

            print(f"Successful: {results['successful']}")
            print(f"Failed:     {results['failed']}")
            print(f"Average:    {results['average_ms']:.3f} ms")
            print(f"Median:     {results['median_ms']:.3f} ms")
            print(f"Minimum:    {results['min_ms']:.3f} ms")
            print(f"Maximum:    {results['max_ms']:.3f} ms")
            print(f"P50:        {results['p50_ms']:.3f} ms")
            print(f"P95:        {results['p95_ms']:.3f} ms")

            db_results[workload_name] = results

    except Exception as exc:
        print(f"FAILED: {db_name} -> {exc}")
        error = exc

    finally:
        adapter.close()

    return db_results, error


def print_summary_table(all_results):
    print(f"\n{'=' * 50}")
    print("Summary")
    print("=" * 50)

    for workload_name in WORKLOADS:
        print(f"\n{workload_name}")
        header = (
            f"{'Database':<12} {'Avg (ms)':>10} {'Median (ms)':>12} "
            f"{'P50 (ms)':>10} {'P95 (ms)':>10}"
        )
        print(header)
        print("-" * len(header))

        for db_name, results in all_results.items():
            stat = results.get(workload_name)
            if not stat:
                print(f"{db_name:<12} {'FAILED':>10}")
                continue
            print(
                f"{db_name:<12} {stat['average_ms']:>10.3f} "
                f"{stat['median_ms']:>12.3f} {stat['p50_ms']:>10.3f} "
                f"{stat['p95_ms']:>10.3f}"
            )


def save_results(all_results):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "all_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved combined results to {path}")


def main():
    all_results = {}
    failures = []

    for db_name, adapter_cls in DATABASES:
        db_results, error = run_database(db_name, adapter_cls)
        all_results[db_name] = db_results
        if error:
            failures.append((db_name, error))

    print_summary_table(all_results)
    save_results(all_results)

    if failures:
        print(f"\n{len(failures)} database(s) failed:")
        for db_name, error in failures:
            print(f"  {db_name}: {error}")


if __name__ == "__main__":
    main()