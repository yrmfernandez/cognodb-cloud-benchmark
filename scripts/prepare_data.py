import csv
import gzip
from pathlib import Path

RAW_DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "wiki-Vote.txt.gz"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

NODES_FILE = PROCESSED_DIR / "nodes.csv"
RELATIONSHIPS_FILE = PROCESSED_DIR / "relationships.csv"

def prepare_data():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    relationships = set()
    nodes = set()

    print(f"Reading raw data from: {RAW_DATA_FILE}")

    with gzip.open(RAW_DATA_FILE, mode='rt', encoding='utf-8') as file:
        for row in file:
            row = row.strip(",")  # Remove leading/trailing whitespace from all values

            if not row or row.startswith('#'):  # Skip empty rows and comments
                continue

            source, target = row.split()

            source = int(source)
            target = int(target)

            nodes.add(source)
            nodes.add(target)

            relationships.add((source, target))

    print(f"nodes found: {len(nodes):,}")
    print(f"relationships found: {len(relationships):,}")

    #writes nodes.csv
    with open(NODES_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            "user_id",
            "user_type"
        ]) 

        # Write header
        for user_id in sorted(nodes):
            user_type = user_id % 10 #logic to determine user type
            writer.writerow([user_id, user_type])

    #writes relationships.csv
    with open(RELATIONSHIPS_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            "source_user_id",
            "target_user_id",
            "relationship_type"
        ])

        for source, target in sorted(relationships):
            writer.writerow([source, target, "VOTED_FOR"])  # Assuming all relationships are of type "VOTED_FOR"

    print()
    print("Data preparation complete.")
    print(f"Nodes written to: {NODES_FILE}")
    print(f"Relationships written to: {RELATIONSHIPS_FILE}")

if __name__ == "__main__":
    prepare_data()
