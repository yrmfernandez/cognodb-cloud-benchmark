from adapters.neo4j import Neo4jAdapter
from workloads import point_lookup
from metrics import measure_workload


def main():
    adapter = Neo4jAdapter()

    try:
        print("Connecting to Neo4j...")
        adapter.connect()
        print("Connected successfully.")

        print("\nRunning Point Lookup benchmark...")
        print("Iterations: 30")

        results = measure_workload(
            workload=lambda adapter: point_lookup(
                adapter,
                user_id=30
            ),
            adapter=adapter,
            iterations=30
        )

        print("\nBenchmark Results")
        print("-----------------")
        print(f"Iterations: {results['iterations']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Average: {results['average_ms']:.3f} ms")
        print(f"Median:  {results['median_ms']:.3f} ms")
        print(f"Minimum: {results['min_ms']:.3f} ms")
        print(f"Maximum: {results['max_ms']:.3f} ms")
        print(f"P95:     {results['p95_ms']:.3f} ms")

    finally:
        adapter.close()


if __name__ == "__main__":
    main()