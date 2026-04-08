from fastapi import FastAPI, Depends, Header, HTTPException, Response
from sqlalchemy.orm import Session
import database
import matplotlib
matplotlib.use('Agg')  # INDISPENSABLE pour serveur
import matplotlib.pyplot as plt
import io
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Import de tes modules IA
import ia_classif
import ia_regress
import ia_clustering

app = FastAPI(title="Cosmetic Pro IA - Final")

# Configuration CORS pour que le navigateur accepte les données
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

database.init_db()
SECRET_KEY = "ABIDJAN_BEAUTY_2026"

@app.get("/", response_class=HTMLResponse)
def read_index():
    return FileResponse("index.html")

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@app.post("/ajouter-vente")
def ajouter(produit: str, teint: str, prix: float, qte: int, age: str, type_peau: str, 
            api_key: str = Header(None, alias="api-key"), db: Session = Depends(get_db)):
    if api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Clé invalide")
    
    mois = datetime.now().month
    saison = "pluie" if mois in [4,5,6,7] else "harmattan" if mois in [12,1,2] else "seche"
    
    nouvelle = database.Vente(
        produit=produit, teint=teint, prix=prix, quantite=qte, 
        age=age, type_peau=type_peau, saison=saison
    )
    db.add(nouvelle)
    db.commit()
    return {"status": "success"}

@app.get("/voir-ventes")
def liste_ventes(db: Session = Depends(get_db)):
    return db.query(database.Vente).all()

# --- LA ROUTE GRAPHIQUE CORRIGÉE ---
@app.get("/graphique-ventes")
def graphique(db: Session = Depends(get_db)):
    ventes = db.query(database.Vente).all()
    
    # On crée une nouvelle figure à chaque fois pour éviter les bugs
    plt.figure(figsize=(8, 5))
    
    if not ventes:
        plt.text(0.5, 0.5, "Aucune donnée disponible", ha='center')
    else:
        noms = [v.produit for v in ventes]
        totaux = [v.prix * v.quantite for v in ventes]
        plt.bar(noms, totaux, color='#db2777') # Rose fuchsia pour le style
        plt.title("Chiffre d'Affaires par Produit")
        plt.xlabel("Produits")
        plt.ylabel("Total (CFA)")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close() # TRÈS IMPORTANT : on ferme la figure pour libérer la mémoire
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

@app.get("/predire-ia")
def route_ia():
    # On appelle tes fonctions IA
    prod = ia_classif.predire_produit("marron", "grasse", "adulte", "pluie", "normal")
    argent = ia_regress.predire_depense("marron", "grasse", "adulte", "pluie", "normal")
    
    return {
        "produit": prod,
        "argent": argent
    }