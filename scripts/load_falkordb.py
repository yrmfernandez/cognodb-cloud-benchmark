import csv
import os
import time

from dotenv import load_dotenv
from falkordb import FalkorDB


load_dotenv()

URI = os.getenv("FALKORDB_URI")
USERNAME = os.getenv("FALKORDB_USERNAME")
PASSWORD = os.getenv("FALKORDB_PASSWORD")

NODES_FILE = "data/processed/nodes.csv"
RELATIONSHIPS_FILE = "data/processed/relationships.csv"

GRAPH_NAME = "benchmark"
BATCH_SIZE = 500


def create_connection():
    if not URI:
        raise ValueError("FALKORDB_URI is missing from .env")

    if not USERNAME:
        raise ValueError("FALKORDB_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("FALKORDB_PASSWORD is missing from .env")

    return FalkorDB.from_url(
        URI,
        username=USERNAME,
        password=PASSWORD,
        socket_connect_timeout=15,
        socket_timeout=30,
    )


def clear_database(graph):
    print("Clearing FalkorDB database...")

    graph.query("""
        MATCH (n)
        DETACH DELETE n
    """)

    print("Database cleared.")


def load_node_batch(graph, batch):
    query = """
    UNWIND $batch AS row
    MERGE (u:User {user_id: row.user_id})
    SET u.user_type = row.user_type
    """

    graph.query(query, params={"batch": batch})


def load_nodes(graph):
    print("Loading nodes from CSV...")

    start_time = time.perf_counter()

    batch = []
    total = 0

    with open(NODES_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            batch.append({
                "user_id": int(row["user_id"]),
                "user_type": int(row["user_type"])
                if row["user_type"] != ""
                else None,
            })

            if len(batch) >= BATCH_SIZE:
                load_node_batch(graph, batch)

                total += len(batch)
                print(f"Nodes loaded: {total:,}")

                batch = []

        if batch:
            load_node_batch(graph, batch)
            total += len(batch)
            print(f"Nodes loaded: {total:,}")

    elapsed = time.perf_counter() - start_time

    print(f"Finished loading {total:,} nodes.")
    print(f"Node load time: {elapsed:.2f} seconds")

    return total, elapsed


def load_relationship_batch(graph, batch):
    query = """
    UNWIND $batch AS row

    MATCH (source:User {user_id: row.source_id})
    MATCH (target:User {user_id: row.target_id})

    CREATE (source)-[:VOTED_FOR]->(target)
    """

    graph.query(query, params={"batch": batch})


def load_relationships(graph):
    print("Loading relationships from CSV...")

    start_time = time.perf_counter()

    batch = []
    total = 0

    with open(RELATIONSHIPS_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            batch.append({
                "source_id": int(row["source_user_id"]),
                "target_id": int(row["target_user_id"]),
            })

            if len(batch) >= BATCH_SIZE:
                load_relationship_batch(graph, batch)

                total += len(batch)
                print(f"Relationships loaded: {total:,}")

                batch = []

        if batch:
            load_relationship_batch(graph, batch)
            total += len(batch)

            print(f"Relationships loaded: {total:,}")

    elapsed = time.perf_counter() - start_time

    print(f"Finished loading {total:,} relationships.")
    print(f"Relationship load time: {elapsed:.2f} seconds")

    return total, elapsed


def verify_database(graph):
    print("\nVerifying FalkorDB database...")

    node_result = graph.query("""
        MATCH (u:User)
        RETURN count(u) AS count
    """)

    relationship_result = graph.query("""
        MATCH ()-[r:VOTED_FOR]->()
        RETURN count(r) AS count
    """)

    node_count = node_result.result_set[0][0]
    relationship_count = relationship_result.result_set[0][0]

    print(f"Database nodes: {node_count:,}")
    print(f"Database relationships: {relationship_count:,}")

    return node_count, relationship_count


def main():
    print("Starting FalkorDB loading process...\n")

    db = create_connection()

    try:
        graph = db.select_graph(GRAPH_NAME)

        # Test connection
        result = graph.query("RETURN 1 AS test")

        print("Connection to FalkorDB successful.")
        print(f"Test query result: {result.result_set[0][0]}\n")

        # Clear existing data
        clear_database(graph)

        print()

        # Load nodes
        node_count, node_time = load_nodes(graph)

        print()

        # Load relationships
        relationship_count, relationship_time = load_relationships(graph)

        # Verify
        verified_nodes, verified_relationships = verify_database(graph)

        print("\nLoad Summary")
        print("----------------------------------------")
        print(f"Nodes:          {node_count:,}")
        print(f"Relationships:  {relationship_count:,}")
        print(f"Node load time: {node_time:.2f} seconds")
        print(f"Relationship load time: {relationship_time:.2f} seconds")

        print("\nVerification Summary")
        print("----------------------------------------")
        print(f"Verified nodes:         {verified_nodes:,}")
        print(f"Verified relationships: {verified_relationships:,}")

        print("\nFalkorDB loading process completed successfully.")

    finally:
        # FalkorDB's Python client manages the underlying connection.
        pass


if __name__ == "__main__":
    main()