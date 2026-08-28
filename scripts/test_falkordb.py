import os

from dotenv import load_dotenv
from falkordb import FalkorDB

load_dotenv()

URI = os.getenv("FALKORDB_URI")
USERNAME = os.getenv("FALKORDB_USERNAME")
PASSWORD = os.getenv("FALKORDB_PASSWORD")

def main():
    if not URI:
        raise ValueError("FALKORDB_URI is missing from .env")

    if not USERNAME:
        raise ValueError("FALKORDB_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("FALKORDB_PASSWORD is missing from .env")

    print(f"Connecting to FalkorDB...")
    print(f"Endpoint: {URI}")

    try:
        db = FalkorDB.from_url(
            URI,
            username=USERNAME,
            password=PASSWORD,
            socket_connect_timeout=30,
            socket_timeout=30,
        )

        graph = db.select_graph("benchmark")

        result = graph.query("RETURN 1 AS test")

        print("Successfully connected to FalkorDB!")
        print(f"Test query result: {result.result_set[0][0]}")

    except Exception as e:
        print(f"FalkorDB connection failed: {type(e).__name__}")
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()