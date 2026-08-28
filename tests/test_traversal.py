
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.neo4j import Neo4jAdapter

adapter = Neo4jAdapter()

try:
    adapter.connect()

    with adapter.driver.session(database=adapter.database) as session:
        result = session.run("SHOW INDEXES")

        for record in result:
            print(record.data())

finally:
    adapter.close()