import socket
import urllib.request
from datetime import datetime

def resolve_dns(host: str) -> dict:
    try:
        ip = socket.gethostbyname(host)
        return {"host": host, "ip": ip, "resolved": True}
    except Exception as e:
        return {"host": host, "ip": None, "resolved": False, "error": str(e)}

def check_http(host: str) -> dict:
    try:
        url = f"https://{host}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "NetDiagAI/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            return {
                "reachable": True,
                "status_code": response.status,
                "message": "Site accessible via HTTPS"
            }
    except urllib.error.HTTPError as e:
        return {
            "reachable": True,
            "status_code": e.code,
            "message": f"Site repond avec code {e.code}"
        }
    except Exception as e:
        return {
            "reachable": False,
            "status_code": None,
            "message": str(e)
        }

def run_scan(target: str) -> dict:
    clean = target.replace("https://", "").replace("http://", "").split("/")[0]

    dns = resolve_dns(clean)
    http = check_http(clean)

    if http["reachable"]:
        status = "healthy"
    elif dns["resolved"]:
        status = "dns_ok_but_http_unreachable"
    else:
        status = "unreachable"

    return {
        "target": target,
        "timestamp": datetime.utcnow().isoformat(),
        "dns": {
            "resolved": dns["resolved"],
            "ip": dns.get("ip"),
        },
        "http": {
            "reachable": http["reachable"],
            "status_code": http.get("status_code"),
            "message": http.get("message"),
        },
        "status": status,
        "summary": f"DNS: {'OK' if dns['resolved'] else 'ECHEC'} | HTTP: {'OK' if http['reachable'] else 'ECHEC'}"
    }