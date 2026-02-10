import os
import csv
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

async def load_csv_to_mongo():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["skylark"]
    
    # Load Pilots CSV
    pilots_path = os.getenv("CSV_PILOTS_PATH", "./data/pilots.csv")
    if os.path.exists(pilots_path):
        await db.pilots.delete_many({})
        with open(pilots_path, 'r') as f:
            reader = csv.DictReader(f)
            pilots = list(reader)
            if pilots:
                await db.pilots.insert_many(pilots)
        print(f"✓ Loaded {len(pilots)} pilots from CSV")
    
    # Load Drones CSV
    drones_path = os.getenv("CSV_DRONES_PATH", "./data/drones.csv")
    if os.path.exists(drones_path):
        await db.drones.delete_many({})
        with open(drones_path, 'r') as f:
            reader = csv.DictReader(f)
            drones = list(reader)
            if drones:
                await db.drones.insert_many(drones)
        print(f"✓ Loaded {len(drones)} drones from CSV")
    
    # Load Projects CSV
    projects_path = os.getenv("CSV_PROJECTS_PATH", "./data/projects.csv")
    if os.path.exists(projects_path):
        await db.projects.delete_many({})
        with open(projects_path, 'r') as f:
            reader = csv.DictReader(f)
            projects = list(reader)
            if projects:
                await db.projects.insert_many(projects)
        print(f"✓ Loaded {len(projects)} projects from CSV")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(load_csv_to_mongo())
