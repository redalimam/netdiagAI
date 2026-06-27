from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Scan
from scanner import run_scan
from ai_diagnosis import generate_diagnosis
import json

router = APIRouter(prefix="/scans", tags=["scans"])

class ScanRequest(BaseModel):
    target: str

@router.post("/run")
def launch_scan(data: ScanRequest, db: Session = Depends(get_db)):
    # 1. Lancer le scan réseau
    print(f"🔍 Scan de {data.target} en cours...")
    scan_result = run_scan(data.target)

    # 2. Générer le diagnostic IA
    print("🤖 Génération du diagnostic IA...")
    diagnosis = generate_diagnosis(scan_result)

    # 3. Sauvegarder en base
    scan = Scan(
        target=data.target,
        result=json.dumps(scan_result),
        diagnosis=json.dumps(diagnosis),
        user_id=None,
        auto=False
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    print(f"✅ Scan #{scan.id} terminé !")
    return {
        "scan_id": scan.id,
        "scan_result": scan_result,
        "diagnosis": diagnosis
    }

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    scans = db.query(Scan).order_by(Scan.created.desc()).limit(10).all()
    return [
        {
            "id": s.id,
            "target": s.target,
            "created": s.created,
            "diagnosis": json.loads(s.diagnosis) if s.diagnosis else None
        }
        for s in scans
    ]

@router.get("/{scan_id}")
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan non trouvé")
    return {
        "id": scan.id,
        "target": scan.target,
        "created": scan.created,
        "scan_result": json.loads(scan.result),
        "diagnosis": json.loads(scan.diagnosis) if scan.diagnosis else None
    }