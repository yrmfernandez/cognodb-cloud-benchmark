import os

import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "results/benchmark_summary.csv"
AVERAGE_OUTPUT_FILE = "results/charts/benchmark_average_latency.png"
P95_OUTPUT_FILE = "results/charts/benchmark_p95_latency.png"


def main():
    df = pd.read_csv(INPUT_FILE)
    os.makedirs("results/charts", exist_ok=True)

    for metric, output_file, title, ylabel in [
        (
            "average_ms",
            AVERAGE_OUTPUT_FILE,
            "Average Query Latency by Database",
            "Average Latency (ms)",
        ),
        (
            "p95_ms",
            P95_OUTPUT_FILE,
            "P95 Query Latency by Database",
            "P95 Latency (ms)",
        ),
    ]:
        pivot = df.pivot(
            index="workload",
            columns="database",
            values=metric
        )

        ax = pivot.plot(
            kind="bar",
            figsize=(12, 7)
        )

        ax.set_title(title)
        ax.set_xlabel("Workload")
        ax.set_ylabel(ylabel)

        plt.xticks(rotation=0)
        plt.legend(title="Database")
        plt.tight_layout()

        plt.savefig(output_file, dpi=300)
        plt.close()

        print(f"Chart saved to: {output_file}")


if __name__ == "__main__":
    main()