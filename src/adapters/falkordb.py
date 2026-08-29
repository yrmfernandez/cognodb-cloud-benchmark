import os

from falkordb import FalkorDB
from dotenv import load_dotenv

from . import DatabaseAdapter


load_dotenv()


class FalkordbAdapter(DatabaseAdapter):
    name = "falkordb"

    def __init__(self):
        self.uri = os.getenv("FALKORDB_URI")
        self.username = os.getenv("FALKORDB_USERNAME")
        self.password = os.getenv("FALKORDB_PASSWORD")
        self.graph_name = os.getenv("FALKORDB_GRAPH", "benchmark")

        if not self.uri:
            raise ValueError("FALKORDB_URI is missing")

        if not self.username:
            raise ValueError("FALKORDB_USERNAME is missing")

        if not self.password:
            raise ValueError("FALKORDB_PASSWORD is missing")

        self.client = None
        self.graph = None

    def connect(self):
        self.client = FalkorDB.from_url(
            self.uri,
            username=self.username,
            password=self.password,
            socket_connect_timeout=15,
            socket_timeout=30,
        )
        self.graph = self.client.select_graph(self.graph_name)
        self.graph.query("RETURN 1 AS test")

    def close(self):
        if self.client:
            self.client.close()

    def point_lookup(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})
        RETURN u.user_id AS user_id,
               u.user_type AS user_type
        """

        result = self.graph.query(query, params={"user_id": user_id})

        if not result.result_set:
            return None

        user_id, user_type = result.result_set[0]
        return {
            "user_id": user_id,
            "user_type": user_type
        }

    def indexed_lookup(self, user_type):
        query = """
        MATCH (u:User {user_type: $user_type})
        RETURN u.user_id AS user_id,
               u.user_type AS user_type
        """

        result = self.graph.query(
            query,
            params={"user_type": user_type}
        )

        return [
            {
                "user_id": row[0],
                "user_type": row[1]
            }
            for row in result.result_set
        ]

    def aggregation(self):
        query = """
        MATCH (u:User)
        RETURN u.user_type AS user_type, count(u) AS user_count
        ORDER BY user_type
        """
        result = self.graph.query(query)
        return [
            {
                "user_type": row[0],
                "user_count": row[1]
            }
            for row in result.result_set
        ]

    def mixed_read_write(self):
        query = """
        MERGE (u:User {user_id: -1})
        SET u.user_type = -1
        WITH u
        RETURN u.user_id AS user_id, u.user_type AS user_type
        """
        cleanup = "MATCH (u:User {user_id: -1}) DELETE u"
        result = self.graph.query(query)
        self.graph.query(cleanup)
        row = result.result_set[0]
        return {"user_id": row[0], "user_type": row[1]}
    
    def hop_1(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:VOTED_FOR]->(v:User)
        RETURN v.user_id AS user_id, v.user_type AS user_type
        """
        result = self.graph.query(query, params={"user_id": user_id})
        return [{"user_id": row[0], "user_type": row[1]} for row in result.result_set]

    def hop_2(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:VOTED_FOR]->()-[:VOTED_FOR]->(v:User)
        RETURN DISTINCT v.user_id AS user_id, v.user_type AS user_type
        """
        result = self.graph.query(query, params={"user_id": user_id})
        return [{"user_id": row[0], "user_type": row[1]} for row in result.result_set]

    def hop_3(self, user_id):
        query = """
        MATCH (u:User {user_id: $user_id})-[:VOTED_FOR]->()-[:VOTED_FOR]->()-[:VOTED_FOR]->(v:User)
        RETURN DISTINCT v.user_id AS user_id, v.user_type AS user_type
        """
        result = self.graph.query(query, params={"user_id": user_id})
        return [{"user_id": row[0], "user_type": row[1]} for row in result.result_set]