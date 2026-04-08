import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans

engine = create_engine("sqlite:///./cosmetique.db")

def segmenter_clients():
    df = pd.read_sql("SELECT * FROM ventes", engine)
    if len(df) < 3: return "Données insuffisantes"

    # On regarde le prix et la quantité
    X = df[['prix', 'quantite']]
    
    # Création de 3 groupes (Petits, Moyens, Gros acheteurs)
    kmeans = KMeans(n_clusters=3, n_init=10)
    df['segment'] = kmeans.fit_predict(X)
    
    # On retourne un résumé pour le Dashboard
    return df[['produit', 'segment']].to_dict(orient="records")