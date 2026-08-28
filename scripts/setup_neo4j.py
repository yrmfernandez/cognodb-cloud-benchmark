import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def main():
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        driver.verify_connectivity()

        with driver.session(database=DATABASE) as session:
            session.run(
                """
                CREATE CONSTRAINT user_id_unique IF NOT EXISTS
                FOR (u:User)
                REQUIRE u.user_id IS UNIQUE
                """
            )

        print("Neo4j constraint created successfully!")

    finally:
        driver.close()


if __name__ == "__main__":
    main()