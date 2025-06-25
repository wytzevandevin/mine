from pathlib import Path

from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect
from tornado.escape import json_encode

from app.api.v1.api import api_router
from app.config import get_settings
from app.database import engine, get_db
from app.models.event import Event

settings = get_settings()

def check_database_connection():
    """
    Check database connection before starting the server.
    """
    try:
        # Create a new session
        session = Session(engine)
        # Try to execute a simple query
        session.execute(text("SELECT 1"))
        session.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def event_table_last_index(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.id.desc()).first()

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

@app.websocket("/ws/truck")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("connected-from server")
    try:
        while True:
            text = await websocket.receive_text()
            print(text)
            # Session = Depends(get_db)
            # data = list_dump(Session)
            await websocket.send_text(json_encode(text))
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    import uvicorn
    # Check database connection before starting the server
    if check_database_connection():
        uvicorn.run("main:app", host="192.168.131.177", port=8000, reload=True)
    else:
        print("Server startup aborted due to database connection failure")