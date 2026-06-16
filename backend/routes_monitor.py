from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import MonitoredTarget
from scanner import run_scan
from ai_diagnosis import generate_diagnosis
from email_alerts import send_alert_email

router = APIRouter(prefix="/monitor", tags=["monitor"])

class TargetData(BaseModel):
    target: str
    email: str

@router.post("/add")
def add_target(data: TargetData, db: Session = Depends(get_db)):
    """Ajouter une cible à surveiller"""
    existing = db.query(MonitoredTarget).filter(
        MonitoredTarget.target == data.target
    ).first()
    if existing:
        return {"message": "Cible déjà surveillée"}
    t = MonitoredTarget(
        target=data.target,
        email=data.email,
        user_id=1
    )
    db.add(t)
    db.commit()
    return {"message": f"{data.target} ajouté à la surveillance", "id": t.id}

@router.get("/list")
def list_targets(db: Session = Depends(get_db)):
    """Liste toutes les cibles surveillées"""
    targets = db.query(MonitoredTarget).all()
    return [{"id": t.id, "target": t.target, "email": t.email} for t in targets]

@router.delete("/remove/{target_id}")
def remove_target(target_id: int, db: Session = Depends(get_db)):
    """Arrêter la surveillance d'une cible"""
    t = db.query(MonitoredTarget).filter(MonitoredTarget.id == target_id).first()
    if t:
        db.delete(t)
        db.commit()
    return {"message": "Cible supprimée"}

@router.post("/test-alert")
def test_alert(data: TargetData):
    """Tester l'envoi d'un email d'alerte"""
    fake_diagnosis = {
        "statut_global": "❌ Réseau inaccessible",
        "score_sante": 10,
        "problemes": [{"titre": "Test alerte", "description": "Ceci est un test", "severite": "critique"}],
        "resume": "Email de test envoyé depuis NetDiagAI."
    }
    send_alert_email(data.target, fake_diagnosis, data.email)
    return {"message": f"Email de test envoyé à {data.email}"}