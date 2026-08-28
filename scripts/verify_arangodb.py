import os

from arango import ArangoClient
from dotenv import load_dotenv


load_dotenv()

URI = os.getenv("ARANGODB_URI")
USERNAME = os.getenv("ARANGODB_USERNAME")
PASSWORD = os.getenv("ARANGODB_PASSWORD")
DATABASE = os.getenv("ARANGODB_DATABASE", "_system")

USER_COLLECTION = "users"
EDGE_COLLECTION = "voted_for"


def create_client():
    if not URI:
        raise ValueError("ARANGODB_URI is missing from .env")

    if not USERNAME:
        raise ValueError("ARANGODB_USERNAME is missing from .env")

    if not PASSWORD:
        raise ValueError("ARANGODB_PASSWORD is missing from .env")

    client = ArangoClient(hosts=URI)

    db = client.db(
        DATABASE,
        username=USERNAME,
        password=PASSWORD
    )

    return client, db


def main():
    client, db = create_client()

    try:
        # Test connection
        version = db.version()

        print("Successfully connected to ArangoDB.")
        print(f"Database: {DATABASE}")
        print(f"ArangoDB version: {version}\n")

        # ---------------------------------------------------------
        # 1. Count the number of nodes
        # ---------------------------------------------------------

        node_query = f"""
        RETURN LENGTH(
            FOR u IN `{USER_COLLECTION}`
                RETURN u
        )
        """

        node_count = next(
            db.aql.execute(node_query)
        )

        print(
            f"Number of nodes in the database: "
            f"{node_count:,}"
        )

        # ---------------------------------------------------------
        # 2. Count the number of relationships
        # ---------------------------------------------------------

        relationship_query = f"""
        RETURN LENGTH(
            FOR r IN `{EDGE_COLLECTION}`
                RETURN r
        )
        """

        relationship_count = next(
            db.aql.execute(relationship_query)
        )

        print(
            f"VOTED_FOR relationships: "
            f"{relationship_count:,}\n"
        )

        # ---------------------------------------------------------
        # 3. Point lookup
        # ---------------------------------------------------------

        point_lookup_query = f"""
        FOR u IN `{USER_COLLECTION}`
            FILTER u.user_id == 30
            RETURN {{
                user_id: u.user_id,
                user_type: u.user_type
            }}
        """

        result = list(
            db.aql.execute(point_lookup_query)
        )

        if result:
            user = result[0]

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

        # ---------------------------------------------------------
        # 4. One-hop neighborhood query
        # ---------------------------------------------------------

        one_hop_query = f"""
        FOR u IN `{USER_COLLECTION}`
            FILTER u.user_id == 30

            FOR target IN 1..1 OUTBOUND
                u
                `{EDGE_COLLECTION}`

            COLLECT WITH COUNT INTO count

            RETURN count
        """

        one_hop_count = next(
            db.aql.execute(one_hop_query)
        )

        print(
            f"1-hop traversal from user 30: "
            f"{one_hop_count} neighbors"
        )

        # ---------------------------------------------------------
        # 5. Verify user_type
        # ---------------------------------------------------------

        typed_users_query = f"""
        RETURN LENGTH(
            FOR u IN `{USER_COLLECTION}`
                FILTER u.user_type != null
                RETURN u
        )
        """

        typed_users = next(
            db.aql.execute(typed_users_query)
        )

        print(
            f"Users with user_type: "
            f"{typed_users:,}"
        )

        # ---------------------------------------------------------
        # Expected values
        # ---------------------------------------------------------

        print("\nVerification Summary")
        print("----------------------------------------")

        checks_passed = True

        if node_count == 7115:
            print("✓ Node count: 7,115")
        else:
            print(
                f"✗ Node count: expected 7,115, "
                f"found {node_count:,}"
            )
            checks_passed = False

        if relationship_count == 103689:
            print("✓ Relationship count: 103,689")
        else:
            print(
                f"✗ Relationship count: expected 103,689, "
                f"found {relationship_count:,}"
            )
            checks_passed = False

        if result and result[0]["user_id"] == 30:
            print("✓ Point lookup: user 30 found")
        else:
            print("✗ Point lookup: user 30 not found")
            checks_passed = False

        if result and result[0]["user_type"] == 0:
            print("✓ User 30 type: 0")
        else:
            print(
                "✗ User 30 type: expected 0"
            )
            checks_passed = False

        if one_hop_count == 5:
            print("✓ 1-hop traversal: 5 neighbors")
        else:
            print(
                f"✗ 1-hop traversal: expected 5, "
                f"found {one_hop_count}"
            )
            checks_passed = False

        if typed_users == 7115:
            print("✓ Users with user_type: 7,115")
        else:
            print(
                f"✗ Users with user_type: expected 7,115, "
                f"found {typed_users:,}"
            )
            checks_passed = False

        if checks_passed:
            print(
                "\nArangoDB verification "
                "completed successfully."
            )
        else:
            print(
                "\nArangoDB verification "
                "completed with errors."
            )

    finally:
        client.close()


if __name__ == "__main__":
    main()