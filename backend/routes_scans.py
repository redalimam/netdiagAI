from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Scan
from scanner import run_scan
import json

router = APIRouter(prefix="/scans", tags=["scans"])

class ScanRequest(BaseModel):
    target: str   # ex: "google.com" ou "192.168.1.1"

@router.post("/run")
def launch_scan(data: ScanRequest, db: Session = Depends(get_db)):
    # Lancer le scan
    result = run_scan(data.target)
    # Sauvegarder en base
    scan = Scan(
        target=data.target,
        result=json.dumps(result),
        user_id=1   # temporaire — on ajoutera l'auth plus tard
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return {"scan_id": scan.id, "result": result}

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    scans = db.query(Scan).order_by(Scan.created.desc()).limit(10).all()
    return [{"id": s.id, "target": s.target, "created": s.created} for s in scans]