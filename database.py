from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Création du fichier de base de données
DATABASE_URL = "sqlite:///./cosmetique.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Vente(Base):
    __tablename__ = "ventes"
    id = Column(Integer, primary_key=True, index=True)
    produit = Column(String)
    teint = Column(String) # Clair, Marron, Noir
    prix = Column(Float)
    quantite = Column(Integer)
    age= Column(String)
    type_peau= Column(String)
    saison=Column(String)
    date_vente = Column(DateTime, default=datetime.datetime.utcnow)
    evenement=Column(String, default="Normal")
def init_db():
    Base.metadata.create_all(bind=engine)