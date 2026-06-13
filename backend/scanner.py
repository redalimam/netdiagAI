import subprocess
import platform
import socket
import json
from datetime import datetime

def ping_host(host: str) -> dict:
    """Teste si un hôte répond et mesure la latence"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "4", host]
    try:
        output = subprocess.run(command, capture_output=True, text=True, timeout=10)
        lines = output.stdout
        # Extraire la latence moyenne
        latency = None
        if "Moyenne" in lines or "Average" in lines:
            for line in lines.split("\n"):
                if "Moyenne" in line or "Average" in line:
                    parts = line.split("=")
                    if len(parts) > 1:
                        latency = parts[-1].strip().replace("ms", "").strip()
        return {
            "host": host,
            "reachable": output.returncode == 0,
            "latency_ms": latency,
            "raw": lines
        }
    except Exception as e:
        return {"host": host, "reachable": False, "error": str(e)}

def resolve_dns(host: str) -> dict:
    """Résout le nom de domaine en IP"""
    try:
        ip = socket.gethostbyname(host)
        return {"host": host, "ip": ip, "resolved": True}
    except:
        return {"host": host, "ip": None, "resolved": False}

def run_scan(target: str) -> dict:
    """Lance un scan complet sur une cible"""
    result = {
        "target": target,
        "timestamp": datetime.utcnow().isoformat(),
        "dns": resolve_dns(target),
        "ping": ping_host(target),
    }
    # Déterminer le statut global
    if result["ping"]["reachable"]:
        result["status"] = "healthy"
    elif result["dns"]["resolved"]:
        result["status"] = "dns_ok_but_unreachable"
    else:
        result["status"] = "unreachable"
    return result