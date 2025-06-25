from pathlib import Path

from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from tornado.escape import json_encode

from app.api.v1.api import api_router
from app.config import get_settings
from app.database import engine, get_db
from app.models.event import Event

settings = get_settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Tarrawonga Story Board application",
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)
last_index=None

# @app.on_event("startup")
# async def start_polling():
#     async def poll_db():
#         global last_index
#         result = event_table_last_index()
#         while True:
#             if result and result.id != last_index:
#                 last_index = result.id

# Serve static files at /static
app.mount("/static", StaticFiles(directory=Path("static"), html=True), name="static")

# Catch-all for React Router (must be after static and API)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    if full_path.startswith("static/") or full_path.startswith("api/"):
        return {"detail": "Not Found"}
    return FileResponse("static/index.html")
@app.get("/")
async def root():
    return {"message": "Welcome to Tarrawonga Story Board API"}

