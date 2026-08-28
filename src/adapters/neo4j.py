import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from . import DatabaseAdapter


load_dotenv()


class Neo4jAdapter(DatabaseAdapter):
    name = "neo4j"

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        if not self.uri:
            raise ValueError("NEO4J_URI is missing")

        if not self.username:
            raise ValueError("NEO4J_USERNAME is missing")

        if not self.password:
            raise ValueError("NEO4J_PASSWORD is missing")

        self.driver = None

    def connect(self):
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

        self.driver.verify_connectivity()

    def close(self):
        if self.driver:
            self.driver.close()

    def point_lookup(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})
        RETURN u.user_id AS user_id,
               u.user_type AS user_type
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                user_id=user_id
            )

            record = result.single()

            if record is None:
                return None

            return {
                "user_id": record["user_id"],
                "user_type": record["user_type"]
            }