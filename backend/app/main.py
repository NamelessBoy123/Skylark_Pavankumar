from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .csv_loader import load_csv_to_mongo
from .api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load CSV data into MongoDB
    await load_csv_to_mongo()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api")
