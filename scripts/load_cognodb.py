import csv
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables from .env file
load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

NODES_FILE = "data/processed/nodes.csv"
RELATIONSHIPS_FILE = "data/processed/relationships.csv"

BATCH_SIZE = 50  # Number of records to process in each batch

def create_driver():
    if not URI:
        raise ValueError("COGNODB_URI is not set in the environment variables.")
    if not USERNAME:
        raise ValueError("COGNODB_USERNAME is not set in the environment variables.")   
    if not PASSWORD:
        raise ValueError("COGNODB_PASSWORD is not set in the environment variables.")

    return GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def clear_database(driver):
    print("Clearing the database...")

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n").consume()

        print("Database cleared.")

def create_constraints(driver):
    print("Creating constraints...")

    with driver.session() as session:
        session.run("""CREATE CONSTRAINT user_id_unique IF NOT EXISTS 
                    FOR (u:User) 
                    REQUIRE u.user_id IS UNIQUE
                    """).consume()

        print("Constraints created.")

def load_nodes(driver):
    print("Loading nodes from CSV...")

    with open(NODES_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        batch = []
        total = 0

        with driver.session() as session:
            for row in reader:
                batch.append(
                    {
                        "user_id": int(row["user_id"]),
                        "user_type": row["user_type"],
                    }
                )

                if len(batch) >= BATCH_SIZE:
                    session.run(
                        """
                        UNWIND $batch AS row
                        MERGE (u:User {user_id: row.user_id})
                        SET u.user_type = row.user_type
                        """,
                        batch=batch,
                    ).consume()

                    total += len(batch)
                    print(f"nodes loaded {total:,}")
                    batch = []

            # Insert/load any remaining nodes
            if batch:
                session.run(
                    """
                    UNWIND $batch AS row
                    MERGE (u:User {user_id: row.user_id})
                    SET u.user_type = row.user_type
                    """,
                    batch=batch,
                ).consume()

                total += len(batch)
    print(f"finished loading {total:,} nodes.")

def load_relationships(driver):
    print("Loading relationships from CSV...")

    with open(RELATIONSHIPS_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        batch = []
        total = 0

        for row in reader:
            batch.append(
                {
                    "source_id": int(row["source_user_id"]),
                    "target_id": int(row["target_user_id"]),
                }
            )

            if len(batch) >= BATCH_SIZE:
                load_relationship_batch(driver, batch)
                total += len(batch)

                print(f"relationships loaded {total:,}")
                batch = []

        #load any remaining relationships
        if batch:
            load_relationship_batch(driver, batch)
            total += len(batch)

            print(f"relationships loaded {total:,}")

    print(f"finished loading {total:,} relationships.")

def load_relationship_batch(driver, batch):
    query = """
    UNWIND $batch AS row
    
    MATCH (source:User {user_id: row.source_user_id})
    MATCH (target:User {user_id: row.target_user_id})

    CREATE (source)-[:VOTED_FOR]->(target)
    """

    for attempt in range(3):  # Retry up to 3 times
        try:
            with driver.session() as session:
                session.run(query, batch=batch).consume()
            break  # Exit the loop if successful
        except Exception as e:
            print(f"Error loading relationships batch: {e}")
            if attempt < 2:  # If not the last attempt, wait and retry
                print("Retrying...")
            else:
                raise  # Raise the exception if all attempts fail
            #reconnect before retrying
            try:
                driver.verify_connectivity()
            except Exception as e:
                pass # If reconnection fails, the next attempt will also fail and raise the exception

def verify_database(driver):
    print("\nverifying database...")

    with driver.session() as session:
        node_result = session.run("MATCH (n:User) RETURN count(n) AS count").single()

        relationship_result = session.run(
            "MATCH ()-[r:VOTED_FOR]->() RETURN count (r) AS count"
        ).single()

        print(f"database nodes: {node_result['count']:,}")
        print(f"database relationships: {relationship_result['count']:,}")

def main():
    print("Starting Cognodb loading process...")

    driver = create_driver()

    try:
        driver.verify_connectivity()
        print("Connection to Cognodb successful.\n")

        clear_database(driver)
        create_constraints(driver)

        load_nodes(driver)
        load_relationships(driver)

        verify_database(driver)

        print("\nCognodb loading process completed successfully.")

    finally:
        driver.close()

if __name__ == "__main__":
    main()