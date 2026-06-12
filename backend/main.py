from fastapi import FastAPI
from database import engine
from models import Base

# Crée automatiquement les tables dans PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NetDiagAI API")

@app.get("/")
def root():
    return {"status": "ok", "message": "NetDiagAI backend fonctionne !"}

@app.get("/health")
def health():
    return {"database": "connectée", "api": "en ligne"}