from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.arangodb import ArangodbAdapter
from src.workloads import point_lookup


def main():
    adapter = ArangodbAdapter()

    try:
        print("Connecting to Arangodb...")
        adapter.connect()
        print("Connected successfully.")

        result = point_lookup(adapter, user_id=30)

        print("\nPoint Lookup Result:")
        print(result)

    finally:
        adapter.close()


if __name__ == "__main__":
    main()