import os

from dotenv import load_dotenv
from falkordb import FalkorDB


load_dotenv()

URI = os.getenv("FALKORDB_URI")
USERNAME = os.getenv("FALKORDB_USERNAME")
PASSWORD = os.getenv("FALKORDB_PASSWORD")

GRAPH_NAME = "benchmark"


def main():
    if not URI:
        raise ValueError("FALKORDB_URI is missing from .env")

    if not USERNAME:
        raise ValueError("FALKORDB_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("FALKORDB_PASSWORD is missing from .env")

    print("Connecting to FalkorDB...")

    db = FalkorDB.from_url(
        URI,
        username=USERNAME,
        password=PASSWORD,
        socket_connect_timeout=15,
        socket_timeout=30,
    )

    graph = db.select_graph(GRAPH_NAME)

    try:
        # Test connection
        result = graph.query("RETURN 1 AS test")

        print("Successfully connected to FalkorDB.")
        print(f"Test query result: {result.result_set[0][0]}\n")

        # 1. Count nodes
        result = graph.query("""
            MATCH (u:User)
            RETURN count(u) AS count
        """)

        node_count = result.result_set[0][0]

        print(f"Number of nodes in the database: {node_count:,}")

        # 2. Count relationships
        result = graph.query("""
            MATCH ()-[r:VOTED_FOR]->()
            RETURN count(r) AS count
        """)

        relationship_count = result.result_set[0][0]

        print(
            f"VOTED_FOR relationships: "
            f"{relationship_count:,}\n"
        )

        # 3. Point lookup
        result = graph.query("""
            MATCH (u:User {user_id: 30})
            RETURN u.user_id AS user_id,
                   u.user_type AS user_type
        """)

        if result.result_set:
            user_id = result.result_set[0][0]
            user_type = result.result_set[0][1]

            print(
                f"Point lookup: user_id={user_id}, "
                f"user_type={user_type}"
            )
        else:
            print("Point lookup: No user found with user_id=30")

        # 4. One-hop neighborhood query
        result = graph.query("""
            MATCH (u:User {user_id: 30})
                  -[:VOTED_FOR]->
                  (target:User)
            RETURN count(target) AS count
        """)

        one_hop_count = result.result_set[0][0]

        print(
            f"1-hop traversal from user 30: "
            f"{one_hop_count} neighbors"
        )

        # 5. Verify user_type
        result = graph.query("""
            MATCH (u:User)
            WHERE u.user_type IS NOT NULL
            RETURN count(u) AS count
        """)

        typed_users = result.result_set[0][0]

        print(
            f"Users with user_type: "
            f"{typed_users:,}"
        )

        # Verification summary
        print("\nVerification Summary")
        print("----------------------------------------")

        print(f"✓ Node count: {node_count:,}")
        print(f"✓ Relationship count: {relationship_count:,}")

        if result:
            print("✓ Point lookup: user 30 found")
            print(f"✓ User 30 type: {user_type}")

        print(
            f"✓ 1-hop traversal: "
            f"{one_hop_count} neighbors"
        )

        print(
            f"✓ Users with user_type: "
            f"{typed_users:,}"
        )

        print("\nFalkorDB verification completed successfully.")

    except Exception as e:
        print(f"FalkorDB verification failed: {e}")
        raise


if __name__ == "__main__":
    main()