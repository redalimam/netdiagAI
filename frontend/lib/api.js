const BASE_URL = "http://localhost:8000";

export async function runScan(target) {
  const res = await fetch(`${BASE_URL}/scans/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target }),
  });
  if (!res.ok) throw new Error("Erreur lors du scan");
  return res.json();
}

export async function getScanHistory() {
  const res = await fetch(`${BASE_URL}/scans/history`);
  if (!res.ok) throw new Error("Erreur historique");
  return res.json();
}

export async function registerUser(email, username, password) {
  const res = await fetch(`${BASE_URL}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, username, password }),
  });
  if (!res.ok) throw new Error("Erreur inscription");
  return res.json();
}

export async function loginUser(email, password) {
  const res = await fetch(`${BASE_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Email ou mot de passe incorrect");
  return res.json();
}