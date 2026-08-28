import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

def test_cognodb_connection():
    if not URI:
        raise ValueError("COGNODB_URI is not set in the environment variables.")
    if not USERNAME:
        raise ValueError("COGNODB_USERNAME is not set in the environment variables.")   
    if not PASSWORD:
        raise ValueError("COGNODB_PASSWORD is not set in the environment variables.")

    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    try:
        driver.verify_connectivity()

        print("Connection to Cognodb successful.")

        with driver.session() as session:
            result = session.run("RETURN 1 AS test")
            record = result.single()

            print(f"Test query result: {record['test']}")

    finally:
        driver.close()

if __name__ == "__main__":
    test_cognodb_connection()