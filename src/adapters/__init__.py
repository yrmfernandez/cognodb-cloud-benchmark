"""
Database adapter definitions.
"""


class DatabaseAdapter:
    """Base interface for all database adapters."""

    name = "unknown"

    def connect(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def point_lookup(self, user_id):
        raise NotImplementedError