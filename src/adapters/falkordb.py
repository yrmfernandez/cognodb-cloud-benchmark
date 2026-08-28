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