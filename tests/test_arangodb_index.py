from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.adapters.arangodb import ArangodbAdapter

adapter = ArangodbAdapter()

try: 
    adapter.connect() 
    print("Connected successfully.") 

    # Create index on user_type 
    index = adapter.db.collection("users").add_index( { "type": "persistent", "fields": ["user_type"], "name": "user_type_index" } ) 

    print("Index:") 
    print(index)

    # Verify indexes 
    print("\nCollection indexes:")

    indexes = adapter.db.collection("users").indexes() 

    for idx in indexes: 
        print(idx)
        
finally: 
    adapter.close()