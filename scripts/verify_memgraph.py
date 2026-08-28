import os

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()

HOST = os.getenv("MEMGRAPH_HOST")
PORT = int(os.getenv("MEMGRAPH_PORT", "7687"))
USERNAME = os.getenv("MEMGRAPH_USERNAME")
PASSWORD = os.getenv("MEMGRAPH_PASSWORD")


def main():
    if not HOST:
        raise ValueError("MEMGRAPH_HOST is missing from .env")

    if not USERNAME:
        raise ValueError("MEMGRAPH_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("MEMGRAPH_PASSWORD is missing from .env")

    connection = Memgraph(
        HOST,
        PORT,
        USERNAME,
        PASSWORD,
        encrypted=True
    )

    try:
        # Test connectivity
        next(
            connection.execute_and_fetch(
                "RETURN 1 AS test"
            )
        )

        print("Successfully connected to Memgraph.\n")

        # 1. Count nodes
        result = connection.execute_and_fetch(
            """
            MATCH (u:User)
            RETURN count(u) AS count
            """
        )

        node_count = next(result)["count"]

        print(
            f"Number of nodes in the database: "
            f"{node_count:,}"
        )

        # 2. Count relationships
        result = connection.execute_and_fetch(
            """
            MATCH ()-[r]->()
            RETURN count(r) AS count
            """
        )

        relationship_count = next(result)["count"]

        print(
            f"VOTED_FOR relationships: "
            f"{relationship_count:,}\n"
        )

        # 3. Point lookup
        result = connection.execute_and_fetch(
            """
            MATCH (u:User {user_id: 30})
            RETURN u.user_id AS user_id,
                   u.user_type AS user_type
            """
        )

        user = next(result, None)

        if user:
            print(
                f"Point lookup: "
                f"user_id={user['user_id']}, "
                f"user_type={user['user_type']}"
            )
        else:
            print(
                "Point lookup: "
                "No user found with user_id=30"
            )

        # 4. One-hop neighborhood query
        result = connection.execute_and_fetch(
            """
            MATCH (u:User {user_id: 30})
                  -[:VOTED_FOR]->(target:User)
            RETURN count(target) AS count
            """
        )

        one_hop_count = next(result)["count"]

        print(
            f"1-hop traversal from user 30: "
            f"{one_hop_count} neighbors"
        )

        # 5. Verify user_type
        result = connection.execute_and_fetch(
            """
            MATCH (u:User)
            WHERE u.user_type IS NOT NULL
            RETURN count(u) AS count
            """
        )

        typed_users = next(result)["count"]

        print(
            f"Users with user_type: "
            f"{typed_users:,}"
        )

        print(
            "\nMemgraph verification "
            "completed successfully."
        )

    finally:
        pass


if __name__ == "__main__":
    main()