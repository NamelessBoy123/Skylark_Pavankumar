from fastapi import APIRouter, Query, HTTPException, Request
from .google_sheets import (
    get_pilots, update_pilot_status, get_drones, update_drone_status,
    get_assignments, sync_assignment, urgent_reassignment, get_projects
)
from .assignment_logic import match_pilot_to_project, detect_conflicts

router = APIRouter()

@router.get("/pilots")
async def pilots(skill: str = None, certification: str = None, location: str = None):
    return await get_pilots(skill, certification, location)

@router.post("/pilot/status")
async def pilot_status(name: str, status: str):
    return await update_pilot_status(name, status)

@router.get("/drones")
async def drones(capability: str = None, location: str = None):
    return await get_drones(capability, location)

@router.post("/drone/status")
async def drone_status(serial: str, status: str):
    return await update_drone_status(serial, status)

@router.get("/assignments")
async def assignments():
    return await get_assignments()

@router.post("/assign")
async def assign(project_id: str):
    return await match_pilot_to_project(project_id)

@router.get("/conflicts")
async def conflicts():
    return await detect_conflicts()

@router.post("/urgent-reassign")
async def urgent_reassign(project_id: str):
    return await urgent_reassignment(project_id)

@router.get("/projects")
async def projects():
    return await get_projects()

@router.post("/agent")
async def agent_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    history = data.get("history", [])
    # Here you would implement your AI logic or rule-based response
    # For now, echo the message or provide a simple rule-based reply
    if "available pilots" in message.lower():
        pilots = await get_pilots()
        reply = f"Available pilots: {', '.join([p.get('name', 'Unknown') for p in pilots])}" if pilots else "No pilots found."
    elif "available drones" in message.lower():
        drones = await get_drones()
        reply = f"Available drones: {', '.join([d.get('model', 'Unknown') for d in drones])}" if drones else "No drones found."
    else:
        reply = "I'm here to help with pilot and drone coordination. Try asking about available pilots or drones."
    return {"reply": reply}
