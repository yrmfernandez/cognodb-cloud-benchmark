import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def main():
    if not URI:
        raise ValueError("NEO4J_URI is missing from .env")

    if not USERNAME:
        raise ValueError("NEO4J_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("NEO4J_PASSWORD is missing from .env")

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    try:
        driver.verify_connectivity()
        print("Successfully connected to Neo4j!")

        database = os.getenv("NEO4J_DATABASE", "neo4j")

        with driver.session(database=database) as session:
            result = session.run("RETURN 1 AS test")
            record = result.single()

            print(f"Test query result: {record['test']}")

    finally:
        driver.close()


if __name__ == "__main__":
    main()