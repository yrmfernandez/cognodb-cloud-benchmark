import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

def main():
    driver = GraphDatabase.driver(URI, 
                                  auth=(USERNAME, PASSWORD)
                                  )

    try:
        driver.verify_connectivity()
        print("Successfully connected to Cognodb. \n")

        with driver.session() as session:

            #1. count the number of nodes in the database
            node_count = session.run("MATCH (u:User) RETURN count(u) AS count").single().get("count")
            print(f"Number of nodes in the database: {node_count}")

            #2. count the number of relationships in the database
            relationship_count = session.run("MATCH ()-[r]->() RETURN count(r) AS count").single().get("count")
            print(f"VOTED FOR relationships:"
                    f"{relationship_count:,} \n")

            #3 Point lookup
            result = session.run("""MATCH (u:User {user_id: 30}) 
                                    RETURN u.user_id AS user_id,
                                            u.user_type AS user_type
                                            """)

            user = result.single()

            if user:
                print(
                    f"Point lookup: user_id={user['user_id']}, "
                    f"user_type={user['user_type']}"
                )
            else:
                print("Point lookup: No user found with user_id=30")

            #4. One-hop neighborhood query
            result = session.run("""MATCH (u:User {user_id: 30})
                                            -[:VOTED_FOR]->(target:User) 
                                    RETURN count(target) AS count
                                            """)

            one_hop_count = result.single()["count"]

            print(
                f"1-hop traversal from user 30: "
                f"{one_hop_count} neighbors"
            )

            #5. verify user_type
            result = session.run("""MATCH (u:User) 
                                    WHERE u.user_type IS NOT NULL
                                    RETURN count(u) AS count
                                """)

            typed_users = result.single()["count"]

            print(
                f"Users with user_type: "
                f"{typed_users: ,} "
            )

        print("\nCognodb verification completed successfully.")

    finally:
        driver.close()

if __name__ == "__main__":
    main()