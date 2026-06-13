from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import User
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/users", tags=["users"])

# Schémas de données (ce qu'on attend du frontend)
class RegisterData(BaseModel):
    email: str
    username: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

# POST /users/register
@router.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    # Créer l'utilisateur
    user = User(
        email=data.email,
        username=data.username,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Compte créé avec succès", "username": user.username}

# POST /users/login
@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    token = create_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "username": user.username}