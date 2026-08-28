import os

from dotenv import load_dotenv
from arango import ArangoClient


load_dotenv()

URI = os.getenv("ARANGODB_URI")
USERNAME = os.getenv("ARANGODB_USERNAME")
PASSWORD = os.getenv("ARANGODB_PASSWORD")
DATABASE = os.getenv("ARANGODB_DATABASE", "_system")


def main():
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

    try:
        version = db.version()

        print("Successfully connected to ArangoDB!")
        print(f"Database: {DATABASE}")
        print(f"ArangoDB version: {version}")

    finally:
        client.close()


if __name__ == "__main__":
    main()