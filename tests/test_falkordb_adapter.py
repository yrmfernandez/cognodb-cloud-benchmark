from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.falkordb import FalkordbAdapter
from src.workloads import point_lookup


def main():
    adapter = FalkordbAdapter()

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