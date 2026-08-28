import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "results/benchmark_summary.csv"
OUTPUT_FILE = "results/benchmark_average_latency.png"


def main():
    df = pd.read_csv(INPUT_FILE)

    pivot = df.pivot(
        index="workload",
        columns="database",
        values="average_ms"
    )

    ax = pivot.plot(
        kind="bar",
        figsize=(12, 7)
    )

    ax.set_title("Average Query Latency by Database")
    ax.set_xlabel("Workload")
    ax.set_ylabel("Average Latency (ms)")

    plt.xticks(rotation=0)
    plt.legend(title="Database")
    plt.tight_layout()

    plt.show()

    plt.savefig(
    "results/charts/benchmark_comparison.png",
    dpi=300,
    bbox_inches="tight"
    )
    
    print(f"Chart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()