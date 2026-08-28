import csv
import os
import time

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()

HOST = os.getenv("MEMGRAPH_HOST")
PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))
USERNAME = os.getenv("MEMGRAPH_USERNAME")
PASSWORD = os.getenv("MEMGRAPH_PASSWORD")

NODES_FILE = "data/processed/nodes.csv"
RELATIONSHIPS_FILE = "data/processed/relationships.csv"

BATCH_SIZE = 500


def create_connection():
    if not HOST:
        raise ValueError("MEMGRAPH_HOST is not set in .env")

    if not USERNAME:
        raise ValueError("MEMGRAPH_USERNAME is not set in .env")

    if not PASSWORD:
        raise ValueError("MEMGRAPH_PASSWORD is not set in .env")

    return Memgraph(
        HOST,
        PORT,
        USERNAME,
        PASSWORD,
        encrypted=True
    )


def clear_database(connection):
    print("Clearing Memgraph database...")

    connection.execute(
        "MATCH (n) DETACH DELETE n"
    )

    print("Database cleared.")


def load_nodes(connection):
    print("Loading nodes from CSV...")

    start_time = time.perf_counter()

    with open(NODES_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        batch = []
        total = 0

        for row in reader:
            batch.append({
                "user_id": int(row["user_id"]),
                "user_type": row["user_type"],
            })

            if len(batch) >= BATCH_SIZE:
                load_node_batch(connection, batch)

                total += len(batch)
                print(f"Nodes loaded: {total:,}")

                batch = []

        if batch:
            load_node_batch(connection, batch)
            total += len(batch)
            print(f"Nodes loaded: {total:,}")

    elapsed = time.perf_counter() - start_time

    print(
        f"Finished loading {total:,} nodes "
        f"in {elapsed:.2f} seconds."
    )

    return elapsed


def load_node_batch(connection, batch):
    query = """
    UNWIND $batch AS row
    CREATE (u:User {
        user_id: row.user_id,
        user_type: row.user_type
    })
    """

    connection.execute(query, {"batch": batch})


def load_relationships(connection):
    print("Loading relationships from CSV...")

    start_time = time.perf_counter()

    with open(
        RELATIONSHIPS_FILE,
        mode="r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        batch = []
        total = 0

        for row in reader:
            batch.append({
                "source_id": int(row["source_user_id"]),
                "target_id": int(row["target_user_id"]),
            })

            if len(batch) >= BATCH_SIZE:
                load_relationship_batch(connection, batch)

                total += len(batch)
                print(f"Relationships loaded: {total:,}")

                batch = []

        if batch:
            load_relationship_batch(connection, batch)
            total += len(batch)

            print(f"Relationships loaded: {total:,}")

    elapsed = time.perf_counter() - start_time

    print(
        f"Finished loading {total:,} relationships "
        f"in {elapsed:.2f} seconds."
    )

    return elapsed


def load_relationship_batch(connection, batch):
    query = """
    UNWIND $batch AS row

    MATCH (source:User {user_id: row.source_id})
    MATCH (target:User {user_id: row.target_id})

    CREATE (source)-[:VOTED_FOR]->(target)
    """

    connection.execute(query, {"batch": batch})


def verify_database(connection):
    print("\nVerifying database...")

    node_result = next(
        connection.execute_and_fetch(
            "MATCH (n:User) RETURN count(n) AS count"
        )
    )

    relationship_result = next(
        connection.execute_and_fetch(
            """
            MATCH ()-[r:VOTED_FOR]->()
            RETURN count(r) AS count
            """
        )
    )

    print(
        f"Database nodes: "
        f"{node_result['count']:,}"
    )

    print(
        f"Database relationships: "
        f"{relationship_result['count']:,}"
    )

    return (
        node_result["count"],
        relationship_result["count"]
    )


def main():
    print("Starting Memgraph loading process...\n")

    connection = create_connection()

    try:
        # Test connection
        next(
            connection.execute_and_fetch(
                "RETURN 1 AS test"
            )
        )

        print("Connection to Memgraph successful.\n")

        clear_database(connection)

        node_time = load_nodes(connection)
        relationship_time = load_relationships(connection)

        node_count, relationship_count = verify_database(
            connection
        )

        print("\nLoad Summary")
        print("-" * 40)
        print(f"Nodes:          {node_count:,}")
        print(f"Relationships:  {relationship_count:,}")
        print(f"Node load time: {node_time:.2f} seconds")
        print(
            f"Relationship load time: "
            f"{relationship_time:.2f} seconds"
        )

        if node_count == 7115 and relationship_count == 103689:
            print("\nMemgraph loading process completed successfully.")
        else:
            print("\nWARNING: Counts do not match expected dataset.")

    finally:
        # GQLAlchemy does not expose close() on the Memgraph object.
        pass


if __name__ == "__main__":
    main()