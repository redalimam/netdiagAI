from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database import SessionLocal
from models import Scan, MonitoredTarget
from scanner import run_scan
from ai_diagnosis import generate_diagnosis
import json

scheduler = BackgroundScheduler()

def scan_all_targets():
    """Lance un scan sur toutes les cibles surveillées"""
    db = SessionLocal()
    try:
        targets = db.query(MonitoredTarget).filter(
            MonitoredTarget.active == True
        ).all()
        for t in targets:
            print(f"Auto-scan de {t.target}...")
            result = run_scan(t.target)
            diagnosis = generate_diagnosis(result)
            scan = Scan(
                target=t.target,
                result=json.dumps(result),
                diagnosis=json.dumps(diagnosis),
                user_id=t.user_id,
                auto=True
            )
            db.add(scan)
            # Vérifier si une alerte doit être envoyée
            if diagnosis.get("score_sante", 100) < 50:
                from email_alerts import send_alert_email
                send_alert_email(t.target, diagnosis, t.email)
        db.commit()
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(
        scan_all_targets,
        IntervalTrigger(minutes=30),
        id="auto_scan",
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler demarré — scan auto toutes les 30 min")