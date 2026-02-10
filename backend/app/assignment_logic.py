from .google_sheets import get_pilots, get_drones, get_assignments, get_projects

def match_pilot_to_project(project_id):
    projects = get_projects()
    project = next((p for p in projects if p.get("project_id") == project_id or str(p.get("_id")) == str(project_id)), None)
    if not project:
        return {"success": False, "message": "Project not found"}

    pilots = get_pilots(skill=project.get("required_skill"))
    if not pilots:
        return {"success": False, "message": "No matching pilots available"}

    pilot = next((p for p in pilots if p.get("status", "").lower() == "available"), pilots[0])

    drones = get_drones(capability=project.get("required_capability"))
    if not drones:
        return {"success": False, "message": "No matching drones available"}

    drone = next((d for d in drones if d.get("status", "").lower() == "available"), drones[0])

    assignment = {
        "project_id": project.get("project_id"),
        "pilot": pilot.get("name"),
        "drone": drone.get("model"),
        "status": "Assigned"
    }
    # Return assignment object; caller should sync to DB if needed
    return {"success": True, "assignment": assignment}

def detect_conflicts():
    assignments = get_assignments()
    conflicts = []

    # Detect simple double-booking by pilot across multiple assignments
    pilot_map = {}
    for a in assignments:
        pilot = a.get("pilot")
        pilot_map.setdefault(pilot, []).append(a.get("project_id"))

    for pilot, projects in pilot_map.items():
        if len(projects) > 1:
            conflicts.append({
                "type": "double_booking",
                "pilot": pilot,
                "projects": projects
            })

    # Additional checks (skill mismatch, drone maintenance) can be added
    return {"conflicts": conflicts}
