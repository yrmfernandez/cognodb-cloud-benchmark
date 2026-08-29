import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from . import DatabaseAdapter


load_dotenv()


class MemgraphAdapter(DatabaseAdapter):
    name = "memgraph"

    def __init__(self):
        self.host = os.getenv("MEMGRAPH_HOST")
        self.port = os.getenv("MEMGRAPH_PORT")
        self.username = os.getenv("MEMGRAPH_USERNAME")
        self.password = os.getenv("MEMGRAPH_PASSWORD")

        if not self.host:
            raise ValueError("MEMGRAPH_HOST is missing")

        if not self.port:
            raise ValueError("MEMGRAPH_PORT is missing")

        if not self.username:
            raise ValueError("MEMGRAPH_USERNAME is missing")

        if not self.password:
            raise ValueError("MEMGRAPH_PASSWORD is missing")

        self.uri = f"bolt+ssc://{self.host}:{self.port}"
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

    def aggregation(self):
        query = """
        MATCH (u:User)
        RETURN u.user_type AS user_type, count(u) AS user_count
        ORDER BY user_type
        """

        with self.driver.session() as session:
            result = session.run(query)
            return result.data()

    def hop_1(self, user_id):
        query = """
        MATCH (u {user_id: $user_id})-[]->(v)
        RETURN v.user_id AS user_id,
        v.user_type AS user_type
        """

        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)

            return [
                {
                    "user_id": record["user_id"],
                    "user_type": record["user_type"]
                }
                for record in result
            ]

    def hop_2(self, user_id):
        query = """
        MATCH (u {user_id: $user_id})
        -[]->()
        -[]->(v)
        RETURN DISTINCT
        v.user_id AS user_id,
        v.user_type AS user_type
        """

        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)

            return [
                {
                    "user_id": record["user_id"],
                    "user_type": record["user_type"]
                }
                for record in result
            ]

    def hop_3(self, user_id):
        query = """
        MATCH (u {user_id: $user_id})
        -[]->()
        -[]->()
        -[]->(v)
        RETURN DISTINCT
        v.user_id AS user_id,
        v.user_type AS user_type
        """

        with self.driver.session() as session:
            result = session.run(query, user_id=user_id)

            return [
                {
                    "user_id": record["user_id"],
                    "user_type": record["user_type"]
                }
                for record in result
            ]