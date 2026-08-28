from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.falkordb import FalkordbAdapter


adapter = FalkordbAdapter()

try:
    adapter.connect()
    print("Connected successfully.")

    # Create index
    adapter.graph.query(
        "CREATE INDEX FOR (u:User) ON (u.user_type)"
    )

    print("Index creation requested.")

    # Verify index
    result = adapter.graph.query(
        "CALL db.indexes()"
    )

    print("\nIndexes:")

    for row in result.result_set:
        print(row)

finally:
    adapter.close()