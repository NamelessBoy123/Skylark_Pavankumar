from .google_sheets import get_pilots, get_drones, get_assignments, get_projects

async def match_pilot_to_project(project_id):
    project = await get_projects()
    project = next((p for p in project if p.get("_id") == project_id), None)
    if not project:
        return {"success": False, "message": "Project not found"}
    
    pilots = await get_pilots(skill=project.get("required_skill"))
    if not pilots:
        return {"success": False, "message": "No matching pilots available"}
    
    # Simple: pick first available
    pilot = pilots[0]
    drones = await get_drones(capability=project.get("required_capability"))
    if not drones:
        return {"success": False, "message": "No matching drones available"}
    
    drone = drones[0]
    
    return {
        "success": True,
        "assignment": {
            "project_id": project_id,
            "pilot": pilot.get("name"),
            "drone": drone.get("model"),
        }
    }

async def detect_conflicts():
    assignments = await get_assignments()
    conflicts = []
    
    for assignment in assignments:
        # Check double-booking
        pilot_assignments = [a for a in assignments if a.get("pilot") == assignment.get("pilot")]
        if len(pilot_assignments) > 1:
            overlapping = any(
                a.get("project_id") != assignment.get("project_id")
                for a in pilot_assignments
            )
            if overlapping:
                conflicts.append({
                    "type": "double_booking",
                    "pilot": assignment.get("pilot"),
                    "projects": [a.get("project_id") for a in pilot_assignments]
                })
    
    return {"conflicts": conflicts}
