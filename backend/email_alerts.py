import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def send_alert_email(target: str, diagnosis: dict, to_email: str):
    """Envoie un email d'alerte quand un problème réseau est détecté"""
    score = diagnosis.get("score_sante", 0)
    statut = diagnosis.get("statut_global", "Problème détecté")
    resume = diagnosis.get("resume", "")

    problemes_html = ""
    for p in diagnosis.get("problemes", []):
        problemes_html += f"""
        

            {p['titre']} — {p['severite']}

            {p['description']}
        
"""

    html = f"""
    

        
⚠️ Alerte Réseau — NetDiagAI

        
Un problème a été détecté sur {target}


        

            
{statut}

            
Score santé : {score}/100


            
{resume}


        

        
Problèmes détectés :

        {problemes_html}
        

            Envoyé automatiquement par NetDiagAI
        


    
"""

    try:
        resend.Emails.send({
            "from": os.getenv("ALERT_FROM_EMAIL", "onboarding@resend.dev"),
            "to": to_email,
            "subject": f"[NetDiagAI] Alerte réseau sur {target}",
            "html": html
        })
        print(f"Email d'alerte envoyé à {to_email}")
    except Exception as e:
        print(f"Erreur envoi email : {e}")