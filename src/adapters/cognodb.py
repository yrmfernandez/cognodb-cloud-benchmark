import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from . import DatabaseAdapter


load_dotenv()


class CognoDBAdapter(DatabaseAdapter):
    name = "cognodb"

    def __init__(self):
        self.uri = os.getenv("COGNODB_URI")
        self.username = os.getenv("COGNODB_USERNAME")
        self.password = os.getenv("COGNODB_PASSWORD")

        if not self.uri:
            raise ValueError("COGNODB_URI is missing")

        if not self.username:
            raise ValueError("COGNODB_USERNAME is missing")

        if not self.password:
            raise ValueError("COGNODB_PASSWORD is missing")

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

        with self.driver.session() as session:
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

    def indexed_lookup(self, user_type):
        query = """
        MATCH (u:User {user_type: $user_type})
        RETURN u.user_id AS user_id,
               u.user_type AS user_type
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                user_type=str(user_type)
            )

            return result.data()

    def hop_1(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:VOTED_FOR]->(v:User)
        RETURN v.user_id AS user_id, v.user_type AS user_type
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            return result.data()

    def hop_2(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:VOTED_FOR]->()-[:VOTED_FOR]->(v:User)
        RETURN DISTINCT v.user_id AS user_id, v.user_type AS user_type
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            return result.data()

    def hop_3(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:VOTED_FOR]->()-[:VOTED_FOR]->()-[:VOTED_FOR]->(v:User)
        RETURN DISTINCT v.user_id AS user_id, v.user_type AS user_type
        """
        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)
            return result.data()