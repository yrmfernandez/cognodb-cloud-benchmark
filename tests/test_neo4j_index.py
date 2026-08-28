
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.neo4j import Neo4jAdapter 

adapter = Neo4jAdapter() 

try: 
    adapter.connect() 
    print("Connected successfully.") 

    with adapter.driver.session(database=adapter.database) as session: 
        # Create index 
        session.run(
            """ 
            CREATE INDEX user_type_index IF NOT EXISTS 
            FOR (u:User) 
            ON (u.user_type) 
        """) 

        print("Index creation requested.") 

        # Verify index 
        
        result = session.run("SHOW INDEXES") 

        for record in result: 
            if record["name"] == "user_type_index": 
                print("Found index:") 
                print(record.data()) 
finally: 
    adapter.close()