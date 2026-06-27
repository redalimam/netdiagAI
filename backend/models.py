from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id       = Column(Integer, primary_key=True, index=True)
    email    = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    plan     = Column(String, default="free")
    created  = Column(DateTime, default=datetime.utcnow)
    scans    = relationship("Scan", back_populates="owner")

class Scan(Base):
    __tablename__ = "scans"
    id         = Column(Integer, primary_key=True, index=True)
    target     = Column(String)   # IP ou domaine scanné
    result     = Column(Text)     # résultat JSON du scan
    diagnosis  = Column(Text)     # rapport IA
    created    = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner      = relationship("User", back_populates="scans")
    auto     = Column(String, default=False)  # True si scan automatique

class MonitoredTarget(Base):
    __tablename__ = "monitored_targets"
    id       = Column(Integer, primary_key=True, index=True)
    target   = Column(String)       # ex: google.com
    email    = Column(String)       # email pour les alertes
    active   = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created  = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id        = Column(Integer, primary_key=True, index=True)
    target    = Column(String)
    message   = Column(Text)
    severity  = Column(String)   # faible / moyenne / critique
    sent     = Column(Boolean, default=False)
    created   = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)