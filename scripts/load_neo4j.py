import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")

BASE_DIR = Path(__file__).resolve().parent.parent
NODES_FILE = BASE_DIR / "data" / "processed" / "nodes.csv"
RELATIONSHIPS_FILE = BASE_DIR / "data" / "processed" / "relationships.csv"

def load_nodes(driver):
    print("Loading nodes...")

    with open(NODES_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        rows = [
            {
                "user_id": int(row["user_id"]),
                "user_type": int(row["user_type"]),
            }
            for row in reader
        ]

    with driver.session(database=DATABASE) as session:
        session.run(
            """
            UNWIND $rows AS row
            MERGE (u:User {user_id: row.user_id})
            SET u.user_type = row.user_type
            """,
            {"rows": rows},
        )

    print(f"Loaded {len(rows)} nodes.")

def load_relationships(driver):
    print("Loading relationships...")

    with open(RELATIONSHIPS_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        rows = [
            {
                "source_user_id": int(row["source_user_id"]),
                "target_user_id": int(row["target_user_id"]),
                "relationship_type": row["relationship_type"],
            }
            for row in reader
        ]

    with driver.session(database=DATABASE) as session:
        session.run(
            """
            UNWIND $rows AS row

            MATCH (source:User {user_id: row.source_user_id})
            MATCH (target:User {user_id: row.target_user_id})

            MERGE (source)-[:VOTED_FOR]->(target)
            """,
            {"rows": rows},
        )

    print(f"Loaded {len(rows)} relationships.")

def main():
    if not URI:
        raise ValueError("NEO4J_URI is missing from .env")

    if not USERNAME:
        raise ValueError("NEO4J_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("NEO4J_PASSWORD is missing from .env")

    if not DATABASE:
        raise ValueError("NEO4J_DATABASE is missing from .env")

    print(f"Connecting to Neo4j Aura...")

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    try:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j!")

        load_nodes(driver)
        load_relationships(driver)

        print("Data loading completed successfully.")

    finally:
        driver.close()

if __name__ == "__main__":
    main()