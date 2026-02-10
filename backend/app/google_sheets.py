import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["skylark"]

def get_pilots(skill=None, certification=None, location=None):
    query = {}
    if skill:
        query["skill_level"] = skill
    if certification:
        # stored as string with commas in CSV; handle both string and list
        query["$or"] = [
            {"certifications": {"$regex": certification, "$options": "i"}},
            {"certifications": {"$in": [certification]}},
        ]
    if location:
        query["current_location"] = location

    pilots = list(db.pilots.find(query))
    return pilots

def update_pilot_status(name, status):
    result = db.pilots.update_one({"name": name}, {"$set": {"status": status}})
    return {"success": result.modified_count > 0}

def get_drones(capability=None, location=None):
    query = {}
    if capability:
        query["$or"] = [
            {"capabilities": {"$regex": capability, "$options": "i"}},
            {"capabilities": {"$in": [capability]}},
        ]
    if location:
        query["current_location"] = location

    drones = list(db.drones.find(query))
    return drones

def update_drone_status(serial, status):
    result = db.drones.update_one({"serial_number": serial}, {"$set": {"status": status}})
    return {"success": result.modified_count > 0}

def get_assignments():
    return list(db.assignments.find({}))

def get_projects():
    return list(db.projects.find({}))

def sync_assignment(assignment):
    result = db.assignments.insert_one(assignment)
    return {"success": True, "id": str(result.inserted_id)}

def urgent_reassignment(project_id):
    # project_id may be project_id string in CSV; try find by project_id field first
    project = db.projects.find_one({"project_id": project_id}) or db.projects.find_one({"_id": ObjectId(project_id)})
    if not project:
        return {"success": False, "message": "Project not found"}
    # Simple placeholder: select first available pilot and drone
    pilot = db.pilots.find_one({"status": {"$regex": "Available", "$options": "i"}})
    drone = db.drones.find_one({"status": {"$regex": "Available", "$options": "i"}})
    if not pilot or not drone:
        return {"success": False, "message": "No available pilot/drone found"}
    assignment = {
        "project_id": project.get("project_id"),
        "pilot": pilot.get("name"),
        "drone": drone.get("model"),
        "status": "Assigned",
    }
    db.assignments.insert_one(assignment)
    return {"success": True, "assignment": assignment}
