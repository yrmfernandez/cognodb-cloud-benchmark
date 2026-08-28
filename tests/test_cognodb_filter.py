from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.cognodb import CognoDBAdapter


adapter = CognoDBAdapter()

try:
    adapter.connect()
    print("Connected successfully.")

    with adapter.driver.session() as session:

        print("\n1. Count all User nodes:")

        result = session.run("""
            MATCH (u:User)
            RETURN count(u) AS count
        """)

        print(result.single()["count"])

        print("\n2. Count user_type = 0:")

        result = session.run("""
            MATCH (u:User)
            WHERE u.user_type = 0
            RETURN count(u) AS count
        """)

        print(result.single()["count"])

        print("\n3. Sample user_type values:")

        result = session.run("""
            MATCH (u:User)
            RETURN u.user_id AS user_id,
                   u.user_type AS user_type
            LIMIT 10
        """)

        print(result.data())

        print("\n4. Property lookup:")

        result = session.run("""
            MATCH (u:User {user_type: 0})
            RETURN u.user_id AS user_id,
                   u.user_type AS user_type
            LIMIT 10
        """)

        print(result.data())

finally:
    adapter.close()