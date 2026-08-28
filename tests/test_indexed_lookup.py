from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.cognodb import CognoDBAdapter
from src.adapters.neo4j import Neo4jAdapter
from src.adapters.memgraph import MemgraphAdapter
from src.adapters.arangodb import ArangodbAdapter
from src.adapters.falkordb import FalkordbAdapter


USER_TYPE = 0

DATABASES = [
    ("cognodb", CognoDBAdapter),
    ("neo4j", Neo4jAdapter),
    ("memgraph", MemgraphAdapter),
    ("arangodb", ArangodbAdapter),
    ("falkordb", FalkordbAdapter),
]


for db_name, adapter_cls in DATABASES:
    print(f"\nTesting {db_name}...")

    adapter = adapter_cls()

    try:
        adapter.connect()
        print("Connected successfully.")

        results = adapter.indexed_lookup(USER_TYPE)

        print(f"user_type={USER_TYPE}: {len(results)} results")

        if results:
            print("Sample:", results[:5])

    except Exception as exc:
        print(f"FAILED: {exc}")

    finally:
        adapter.close()