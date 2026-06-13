from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_diagnosis(scan_result: dict) -> dict:
    scan_summary = json.dumps(scan_result, indent=2, ensure_ascii=False)

    prompt = f"""Tu es un expert en réseaux et télécommunications.
Analyse ce résultat de scan réseau et génère un rapport clair et structuré.

DONNÉES DU SCAN :
{scan_summary}

Réponds UNIQUEMENT avec un objet JSON valide (sans markdown, sans backticks) avec cette structure exacte :
{{
  "statut_global": "✅ Réseau sain" ou "⚠️ Problèmes détectés" ou "❌ Réseau inaccessible",
  "score_sante": un nombre entre 0 et 100,
  "problemes": [
    {{ "titre": "...", "description": "...", "severite": "faible/moyenne/critique" }}
  ],
  "recommandations": [
    {{ "action": "...", "priorite": "haute/moyenne/basse", "detail": "..." }}
  ],
  "resume": "Un paragraphe résumant l'état du réseau en langage simple"
}}

Si le réseau est sain, mets une liste vide pour problemes.
Réponds en français."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )

    response_text = response.choices[0].message.content.strip()

    # Nettoyer si backticks markdown
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        response_text = "\n".join(lines)

    try:
        diagnosis = json.loads(response_text)
    except json.JSONDecodeError:
        diagnosis = {
            "statut_global": "⚠️ Analyse partielle",
            "score_sante": 50,
            "problemes": [],
            "recommandations": [],
            "resume": response_text
        }

    return diagnosis