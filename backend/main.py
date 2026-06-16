from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes_users import router as users_router
from routes_scans import router as scans_router
from routes_monitor import router as monitor_router
from scheduler import start_scheduler


Base.metadata.create_all(bind=engine)

app = FastAPI(title="NetDiagAI API")

# Autoriser le frontend React à parler au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(scans_router)
app.include_router(monitor_router)
@app.get("/")
def root():
    return {"status": "ok", "message": "NetDiagAI backend fonctionne !"}
@app.on_event("startup")
def startup_event():
    start_scheduler()