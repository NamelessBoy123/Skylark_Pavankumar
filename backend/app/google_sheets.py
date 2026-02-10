import os
import gspread
from google.oauth2.service_account import Credentials
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["skylark"]

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), scopes=SCOPES)
gc = gspread.authorize(CREDS)

PILOT_SHEET = os.getenv("PILOT_SHEET_ID")
DRONE_SHEET = os.getenv("DRONE_SHEET_ID")

async def get_pilots(skill=None, certification=None, location=None):
    # For demo, return mock data
    return [
        {"name": "Alice", "status": "Available"},
        {"name": "Bob", "status": "On Leave"},
    ]

async def update_pilot_status(name, status):
    # Update in MongoDB and Google Sheets
    # ...implement update logic...
    return {"success": True}

async def get_drones(capability=None, location=None):
    # For demo, return mock data
    return [
        {"model": "DJI Phantom", "status": "Available"},
        {"model": "Parrot Anafi", "status": "Maintenance"},
    ]

async def update_drone_status(serial, status):
    # Update in MongoDB and Google Sheets
    # ...implement update logic...
    return {"success": True}

async def get_assignments():
    # Query assignments from MongoDB
    return []

async def sync_assignment(assignment):
    # Sync assignment to Google Sheets
    return {"success": True}

async def urgent_reassignment(project_id):
    # Find replacement pilot/drone and update assignment
    return {"success": True, "message": "Urgent reassignment handled"}
