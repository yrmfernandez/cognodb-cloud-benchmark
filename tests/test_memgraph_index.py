from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.memgraph import MemgraphAdapter

adapter = MemgraphAdapter() 

try: 
    adapter.connect() 
    print("Connected successfully.") 

    with adapter.driver.session() as session: 

        # Create index 
        session.run(""" CREATE INDEX ON :User(user_type) """) 
        print("Index creation requested.") 
        
        # Verify indexes 
        result = session.run("SHOW INDEX INFO") 

        for record in result: 
            print(record) 

finally: 
    adapter.close()