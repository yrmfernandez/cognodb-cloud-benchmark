from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.cognodb import CognoDBAdapter


adapter = CognoDBAdapter()

try:
    adapter.connect()
    print("Connected successfully.")

    with adapter.driver.session() as session:

        # Create index
        session.run("""
            CREATE INDEX user_type_index
            FOR (u:User)
            ON (u.user_type)
        """)

        print("Index creation requested.")

        # Verify indexes
        result = session.run("SHOW INDEXES")

        print("\nIndexes:")

        for record in result:
            print(record.data())

finally:
    adapter.close()