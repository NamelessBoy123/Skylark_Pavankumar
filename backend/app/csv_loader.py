import os
import csv
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
CSV_PILOTS_PATH = os.getenv("CSV_PILOTS_PATH", "./data/pilots.csv")
CSV_DRONES_PATH = os.getenv("CSV_DRONES_PATH", "./data/drone_fleet.csv")
CSV_PROJECTS_PATH = os.getenv("CSV_PROJECTS_PATH", "./data/projects.csv")

def load_csv_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client["skylark"]

    # Pilots
    if os.path.exists(CSV_PILOTS_PATH):
        with open(CSV_PILOTS_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            pilots = list(reader)
            if pilots:
                db.pilots.delete_many({})
                db.pilots.insert_many(pilots)
        print(f"✓ Loaded {len(pilots)} pilots from CSV")

    # Drones
    if os.path.exists(CSV_DRONES_PATH):
        with open(CSV_DRONES_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            drones = list(reader)
            if drones:
                db.drones.delete_many({})
                db.drones.insert_many(drones)
        print(f"✓ Loaded {len(drones)} drones from CSV")

    # Projects
    if os.path.exists(CSV_PROJECTS_PATH):
        with open(CSV_PROJECTS_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            projects = list(reader)
            if projects:
                db.projects.delete_many({})
                db.projects.insert_many(projects)
        print(f"✓ Loaded {len(projects)} projects from CSV")

    client.close()

if __name__ == "__main__":
    load_csv_to_mongo()
