from adapters.memgraph import MemgraphAdapter
from workloads import point_lookup


def main():
    adapter = MemgraphAdapter()

    try:
        print("Connecting to Memgraph...")
        adapter.connect()
        print("Connected successfully.")

        result = point_lookup(adapter, user_id=30)

        print("\nPoint Lookup Result:")
        print(result)

    finally:
        adapter.close()


if __name__ == "__main__":
    main()