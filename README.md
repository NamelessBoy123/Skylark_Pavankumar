# Skylark Drone Operations Coordinator AI

A full-stack application for managing drone pilots, fleet inventory, assignments, and conflict detection.

## Architecture

- **Backend:** FastAPI (Python) + MongoDB Atlas
- **Frontend:** React (TypeScript)
- **Data:** CSV files loaded into MongoDB on startup
- **Deployment:** Docker + GitHub Actions + AWS

## Setup

### Prerequisites
- Docker & Docker Compose
- MongoDB Atlas account
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Environment Variables

Create `.env` in project root:
```
MONGO_URI=mongodb+srv://pes1202203580_db_user:<db_password>@cluster0.hxezo3e.mongodb.net/skylark?retryWrites=true&w=majority
PILOT_SHEET_ID=your_google_sheet_id
DRONE_SHEET_ID=your_google_sheet_id
```

### Local Development

```bash
# Build and run
docker-compose up --build

# Frontend: http://localhost
# Backend API Docs: http://localhost:8000/docs
```

### CSV Data Files

Place your CSV files in the `data/` directory:
- `pilots.csv` - Pilot roster
- `drones.csv` - Drone fleet
- `projects.csv` - Project assignments

CSV files are auto-loaded into MongoDB on backend startup.

## Features

1. **Roster Management** - Query pilots by skill, certification, location
2. **Assignment Tracking** - Match pilots/drones to projects
3. **Drone Inventory** - Track fleet status and capabilities
4. **Conflict Detection** - Detect double-booking, skill mismatches, location issues
5. **Urgent Reassignment** - Coordinate emergency pilot/drone swaps

## API Endpoints

- `GET /api/pilots` - List pilots (filters: skill, certification, location)
- `POST /api/pilot/status` - Update pilot status
- `GET /api/drones` - List drones (filters: capability, location)
- `POST /api/drone/status` - Update drone status
- `GET /api/assignments` - List assignments
- `POST /api/assign` - Create assignment
- `GET /api/conflicts` - Detect conflicts
- `POST /api/agent` - Conversational AI interface
- `POST /api/urgent-reassign` - Handle urgent reassignments

## Folder Structure

```
Skylark_Assigment/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api.py
│   │   ├── google_sheets.py
│   │   ├── assignment_logic.py
│   │   └── csv_loader.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── data/
│   ├── pilots.csv
│   ├── drones.csv
│   └── projects.csv
├── docker-compose.yml
├── .env
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── README.md
```

## Troubleshooting

- **Frontend build fails:** Clear node_modules and reinstall: `npm install`
- **MongoDB connection error:** Verify MONGO_URI in .env and whitelist your IP in Atlas
- **Backend health check fails:** Check logs: `docker logs skylark_backend`

## Deployment

Push to GitHub with secrets configured:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `MONGO_URI`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

CI/CD pipeline will auto-build and push to DockerHub.
