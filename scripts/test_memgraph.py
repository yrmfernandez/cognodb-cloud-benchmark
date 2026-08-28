import os

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()

HOST = os.getenv("MEMGRAPH_HOST")
PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))
USERNAME = os.getenv("MEMGRAPH_USERNAME")
PASSWORD = os.getenv("MEMGRAPH_PASSWORD")


def main():
    if not HOST:
        raise ValueError("MEMGRAPH_HOST is missing from .env")

    if not USERNAME:
        raise ValueError("MEMGRAPH_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("MEMGRAPH_PASSWORD is missing from .env")

    connection = Memgraph(
        HOST,
        PORT,
        USERNAME,
        PASSWORD,
        encrypted=True
    )

    results = connection.execute_and_fetch(
        "RETURN 1 AS test"
    )

    record = next(results)

    print("Successfully connected to Memgraph!")
    print(f"Test query result: {record['test']}")


if __name__ == "__main__":
    main()