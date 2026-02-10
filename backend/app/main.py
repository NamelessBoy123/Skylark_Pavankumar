from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from . import csv_loader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    try:
        csv_loader.load_csv_to_mongo()
    except Exception as e:
        # Log but don't crash — helps when DB not reachable during container startup
        print("Warning: CSV load failed on startup:", str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api")
