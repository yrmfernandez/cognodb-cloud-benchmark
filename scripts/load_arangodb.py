import csv
import os
import time

from arango import ArangoClient
from dotenv import load_dotenv


load_dotenv()

URI = os.getenv("ARANGODB_URI")
USERNAME = os.getenv("ARANGODB_USERNAME")
PASSWORD = os.getenv("ARANGODB_PASSWORD")
DATABASE = os.getenv("ARANGODB_DATABASE", "_system")

NODES_FILE = "data/processed/nodes.csv"
RELATIONSHIPS_FILE = "data/processed/relationships.csv"

BATCH_SIZE = 500

USER_COLLECTION = "users"
EDGE_COLLECTION = "voted_for"


def create_client():
    if not URI:
        raise ValueError("ARANGODB_URI is missing from .env")

    if not USERNAME:
        raise ValueError("ARANGODB_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("ARANGODB_PASSWORD is missing from .env")

    client = ArangoClient(hosts=URI)

    db = client.db(
        DATABASE,
        username=USERNAME,
        password=PASSWORD
    )

    return client, db


def clear_database(db):
    print("Clearing ArangoDB collections...")

    if db.has_collection(EDGE_COLLECTION):
        db.delete_collection(EDGE_COLLECTION)

    if db.has_collection(USER_COLLECTION):
        db.delete_collection(USER_COLLECTION)

    print("Database cleared.")


def create_collections(db):
    print("Creating collections...")

    db.create_collection(USER_COLLECTION)

    db.create_collection(
        EDGE_COLLECTION,
        edge=True
    )

    print("Collections created.")


def load_nodes(db):
    print("Loading nodes from CSV...")

    start_time = time.perf_counter()

    collection = db.collection(USER_COLLECTION)

    batch = []
    total = 0

    with open(NODES_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            batch.append(
                {
                    "_key": str(row["user_id"]),
                    "user_id": int(row["user_id"]),
                    "user_type": int(row["user_type"]),
                }
            )

            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                total += len(batch)

                print(f"Nodes loaded: {total:,}")

                batch = []

        if batch:
            collection.insert_many(batch)
            total += len(batch)

            print(f"Nodes loaded: {total:,}")

    elapsed = time.perf_counter() - start_time

    print(f"Finished loading {total:,} nodes.")
    print(f"Node load time: {elapsed:.2f} seconds")

    return elapsed


def load_relationships(db):
    print("Loading relationships from CSV...")

    start_time = time.perf_counter()

    collection = db.collection(EDGE_COLLECTION)

    batch = []
    total = 0

    with open(RELATIONSHIPS_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            source_id = str(row["source_user_id"])
            target_id = str(row["target_user_id"])

            batch.append(
                {
                    "_from": f"{USER_COLLECTION}/{source_id}",
                    "_to": f"{USER_COLLECTION}/{target_id}",
                    "relationship_type": row["relationship_type"],
                }
            )

            if len(batch) >= BATCH_SIZE:
                collection.insert_many(batch)
                total += len(batch)

                print(f"Relationships loaded: {total:,}")

                batch = []

        if batch:
            collection.insert_many(batch)
            total += len(batch)

            print(f"Relationships loaded: {total:,}")

    elapsed = time.perf_counter() - start_time

    print(f"Finished loading {total:,} relationships.")
    print(f"Relationship load time: {elapsed:.2f} seconds")

    return elapsed


def verify_database(db):
    print("\nVerifying database...")

    users = db.collection(USER_COLLECTION)
    relationships = db.collection(EDGE_COLLECTION)

    node_count = users.count()

    relationship_count = relationships.count()

    print(f"Database nodes: {node_count:,}")
    print(f"Database relationships: {relationship_count:,}")

    return node_count, relationship_count


def main():
    print("Starting ArangoDB loading process...\n")

    client, db = create_client()

    try:
        # Test connection
        db.version()

        print("Connection to ArangoDB successful.\n")

        clear_database(db)

        create_collections(db)

        node_start = time.perf_counter()
        node_time = load_nodes(db)
        node_elapsed = time.perf_counter() - node_start

        relationship_start = time.perf_counter()
        relationship_time = load_relationships(db)
        relationship_elapsed = time.perf_counter() - relationship_start

        node_count, relationship_count = verify_database(db)

        print("\nLoad Summary")
        print("----------------------------------------")
        print(f"Nodes:          {node_count:,}")
        print(f"Relationships:  {relationship_count:,}")
        print(f"Node load time: {node_time:.2f} seconds")
        print(
            f"Relationship load time: "
            f"{relationship_time:.2f} seconds"
        )

        if node_count != 7115:
            raise RuntimeError(
                f"Expected 7,115 nodes but found {node_count:,}"
            )

        if relationship_count != 103689:
            raise RuntimeError(
                "Expected 103,689 relationships "
                f"but found {relationship_count:,}"
            )

        print(
            "\nArangoDB loading process "
            "completed successfully."
        )

    finally:
        client.close()


if __name__ == "__main__":
    main()