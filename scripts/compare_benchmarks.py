"""Generate reproducible benchmark comparison tables from combined JSON results."""

import argparse
import csv
import json
from pathlib import Path


DEFAULT_INPUT = Path("results/all_results.json")
DEFAULT_OUTPUT_DIR = Path("results/comparison")
WORKLOADS = (
    ("point_lookup", "Point Lookup"),
    ("hop_1", "1-Hop Traversal"),
    ("hop_2", "2-Hop Traversal"),
    ("hop_3", "3-Hop Traversal"),
    ("indexed_lookup", "Indexed Lookup"),
    ("aggregation", "Aggregation"),
)
METRICS = ("average_ms", "p95_ms")


def project_root():
    return Path(__file__).resolve().parent.parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare benchmark results from results/all_results.json."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=project_root() / DEFAULT_INPUT,
        help="Path to the combined benchmark JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_root() / DEFAULT_OUTPUT_DIR,
        help="Directory for generated comparison files.",
    )
    return parser.parse_args()


def load_results(input_path):
    with input_path.open("r", encoding="utf-8") as file:
        results = json.load(file)

    if not isinstance(results, dict) or not results:
        raise ValueError("Benchmark results must contain at least one database.")

    for database, database_results in results.items():
        for workload_key, _ in WORKLOADS:
            metrics = database_results.get(workload_key)
            if not isinstance(metrics, dict):
                raise ValueError(
                    f"Missing workload '{workload_key}' for database '{database}'."
                )
            for metric in METRICS:
                if metric not in metrics:
                    raise ValueError(
                        f"Missing metric '{metric}' for {database}/{workload_key}."
                    )

    return results


def build_rows(results):
    average_rows = []
    p95_rows = []
    relative_rows = []

    for workload_key, workload_name in WORKLOADS:
        values = {
            database: database_results[workload_key]
            for database, database_results in results.items()
        }
        fastest_average = min(
            metrics["average_ms"] for metrics in values.values()
        )
        fastest_p95 = min(metrics["p95_ms"] for metrics in values.values())
        average_order = sorted(
            values.items(), key=lambda item: item[1]["average_ms"]
        )

        for rank, (database, metrics) in enumerate(average_order, start=1):
            average_rows.append(
                {
                    "workload": workload_key,
                    "workload_name": workload_name,
                    "rank": rank,
                    "database": database,
                    "average_ms": metrics["average_ms"],
                    "fastest": metrics["average_ms"] == fastest_average,
                }
            )

        for database, metrics in values.items():
            relative_rows.append(
                {
                    "workload": workload_key,
                    "workload_name": workload_name,
                    "database": database,
                    "average_ms": metrics["average_ms"],
                    "relative_to_best_pct": (
                        (metrics["average_ms"] - fastest_average)
                        / metrics["average_ms"]
                        * 100
                    ),
                    "p95_ms": metrics["p95_ms"],
                    "p95_relative_to_best_pct": (
                        (metrics["p95_ms"] - fastest_p95)
                        / metrics["p95_ms"]
                        * 100
                    ),
                    "fastest_average": metrics["average_ms"] == fastest_average,
                    "fastest_p95": metrics["p95_ms"] == fastest_p95,
                }
            )

        p95_rows.append(
            {
                "workload": workload_key,
                "workload_name": workload_name,
                **{
                    database: metrics["p95_ms"]
                    for database, metrics in values.items()
                },
            }
        )

    return average_rows, p95_rows, relative_rows


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def format_ms(value):
    return f"{value:,.2f} ms"


def format_pct(value):
    return f"{value:.2f}%"


def build_report(average_rows, p95_rows, relative_rows):
    lines = [
        "# Benchmark Comparison",
        "",
        "Generated from `results/all_results.json` by `scripts/compare_benchmarks.py`.",
        "",
        "## Average Latency",
        "",
        "Lower latency is better.",
        "",
        "| Rank | Database | " + " | ".join(
            workload_name for _, workload_name in WORKLOADS
        ) + " |",
        "|---:|---|" + "---:|" * len(WORKLOADS),
    ]

    databases = sorted(
        {row["database"] for row in average_rows},
        key=lambda database: next(
            row["rank"]
            for row in average_rows
            if row["database"] == database and row["workload"] == "point_lookup"
        ),
    )
    average_by_key = {
        (row["database"], row["workload"]): row for row in average_rows
    }

    for rank, database in enumerate(databases, start=1):
        values = [
            format_ms(average_by_key[(database, workload_key)]["average_ms"])
            for workload_key, _ in WORKLOADS
        ]
        lines.append(f"| {rank} | {database} | " + " | ".join(values) + " |")

    lines.extend(["", "## Relative Performance", ""])
    lines.append(
        "Percentage slower is calculated relative to the best result for each workload: "
        "`((database latency - best latency) / database latency) * 100`."
    )
    lines.extend(["", "| Workload | Database | Average | Relative to best |", "|---|---|---:|---:|"])

    for row in sorted(relative_rows, key=lambda item: (item["workload"], item["average_ms"])):
        relative = "Best" if row["fastest_average"] else format_pct(row["relative_to_best_pct"])
        lines.append(
            f"| {row['workload_name']} | {row['database']} | "
            f"{format_ms(row['average_ms'])} | {relative} |"
        )

    lines.extend(["", "## P95 Latency", "", "| Workload | " + " | ".join(
        database for database in databases
    ) + " |", "|---|" + "---:|" * len(databases)])

    for row in p95_rows:
        lines.append(
            f"| {row['workload_name']} | "
            + " | ".join(format_ms(row[database]) for database in databases)
            + " |"
        )

    return "\n".join(lines) + "\n"


def main():
    args = parse_args()
    input_path = args.input.resolve()
    output_dir = args.output_dir.resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Benchmark results not found: {input_path}")

    results = load_results(input_path)
    average_rows, p95_rows, relative_rows = build_rows(results)
    output_dir.mkdir(parents=True, exist_ok=True)

    write_csv(
        output_dir / "average_latency.csv",
        average_rows,
        ["workload", "workload_name", "rank", "database", "average_ms", "fastest"],
    )
    write_csv(
        output_dir / "p95_latency.csv",
        p95_rows,
        ["workload", "workload_name", *sorted(results)],
    )
    write_csv(
        output_dir / "relative_performance.csv",
        relative_rows,
        [
            "workload",
            "workload_name",
            "database",
            "average_ms",
            "relative_to_best_pct",
            "p95_ms",
            "p95_relative_to_best_pct",
            "fastest_average",
            "fastest_p95",
        ],
    )
    (output_dir / "comparison_report.md").write_text(
        build_report(average_rows, p95_rows, relative_rows), encoding="utf-8"
    )

    print(f"Loaded: {input_path}")
    print(f"Generated comparison files in: {output_dir}")


if __name__ == "__main__":
    main()
