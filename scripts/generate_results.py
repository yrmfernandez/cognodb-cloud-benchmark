import json
import csv
import os


INPUT_FILE = "results/all_results.json"
OUTPUT_FILE = "results/benchmark_summary.csv"


def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Could not find benchmark results: {INPUT_FILE}"
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)

    rows = []

    for database, database_results in results.items():

        for workload, metrics in database_results.items():

            if workload == "database":
                continue

            rows.append({
                "database": database,
                "workload": workload,
                "iterations": metrics["iterations"],
                "warmup_iterations": metrics["warmup_iterations"],
                "successful": metrics["successful"],
                "failed": metrics["failed"],
                "average_ms": metrics["average_ms"],
                "median_ms": metrics["median_ms"],
                "min_ms": metrics["min_ms"],
                "max_ms": metrics["max_ms"],
                "p50_ms": metrics["p50_ms"],
                "p95_ms": metrics["p95_ms"],
            })

    os.makedirs("results", exist_ok=True)

    fieldnames = [
        "database",
        "workload",
        "iterations",
        "warmup_iterations",
        "successful",
        "failed",
        "average_ms",
        "median_ms",
        "min_ms",
        "max_ms",
        "p50_ms",
        "p95_ms",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print("Benchmark summary generated successfully.")
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total benchmark rows: {len(rows)}")


if __name__ == "__main__":
    main()