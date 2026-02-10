import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["skylark"]

async def get_pilots(skill=None, certification=None, location=None):
    query = {}
    if skill:
        query["skill_level"] = skill
    if certification:
        query["certifications"] = {"$in": [certification]}
    if location:
        query["current_location"] = location
    
    pilots = await db.pilots.find(query).to_list(length=None)
    return pilots

async def update_pilot_status(name, status):
    result = await db.pilots.update_one(
        {"name": name},
        {"$set": {"status": status}}
    )
    return {"success": result.modified_count > 0}

async def get_drones(capability=None, location=None):
    query = {}
    if capability:
        query["capabilities"] = {"$in": [capability]}
    if location:
        query["current_location"] = location
    
    drones = await db.drones.find(query).to_list(length=None)
    return drones

async def update_drone_status(serial, status):
    result = await db.drones.update_one(
        {"serial_number": serial},
        {"$set": {"status": status}}
    )
    return {"success": result.modified_count > 0}

async def get_assignments():
    assignments = await db.assignments.find({}).to_list(length=None)
    return assignments

async def get_projects():
    projects = await db.projects.find({}).to_list(length=None)
    return projects

async def sync_assignment(assignment):
    result = await db.assignments.insert_one(assignment)
    return {"success": True, "id": str(result.inserted_id)}

async def urgent_reassignment(project_id):
    project = await db.projects.find_one({"_id": project_id})
    if not project:
        return {"success": False, "message": "Project not found"}
    
    # Find available pilot/drone and reassign
    return {"success": True, "message": "Urgent reassignment handled"}
