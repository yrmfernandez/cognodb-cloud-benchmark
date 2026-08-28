import os

from arango import ArangoClient
from dotenv import load_dotenv

from . import DatabaseAdapter


load_dotenv()


class ArangodbAdapter(DatabaseAdapter):
    name = "arangodb"

    def __init__(self):
        self.uri = os.getenv("ARANGODB_URI")
        self.username = os.getenv("ARANGODB_USERNAME")
        self.password = os.getenv("ARANGODB_PASSWORD")
        self.database = os.getenv("ARANGODB_DATABASE")

        if not self.uri:
            raise ValueError("ARANGODB_URI is missing")

        if not self.username:
            raise ValueError("ARANGODB_USERNAME is missing")

        if not self.password:
            raise ValueError("ARANGODB_PASSWORD is missing")

        if not self.database:
            raise ValueError("ARANGODB_DATABASE is missing")

        self.client = None
        self.db = None

    def connect(self):
        self.client = ArangoClient(hosts=self.uri)
        self.db = self.client.db(
            self.database,
            username=self.username,
            password=self.password
        )

        self.db.version()

    def close(self):
        if self.client:
            self.client.close()

    def point_lookup(self, user_id):
        query = """
        FOR u IN users
            FILTER u.user_id == @user_id
            RETURN {
                user_id: u.user_id,
                user_type: u.user_type
            }
        """

        result = self.db.aql.execute(
            query,
            bind_vars={"user_id": user_id}
        )
        return next(result, None)