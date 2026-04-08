import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

# 1. Connexion à la base
engine = create_engine("sqlite:///./cosmetique.db")

def predire_depense(teint, peau, age, saison, event):
    # ON CRÉE LE DF ICI D'ABORD
    try:
        df = pd.read_sql("SELECT * FROM ventes", engine)
    except Exception:
        return 0

    # Si la base est vide ou trop petite
    if df.empty or len(df) < 2:
        return 0

    # 2. MAINTENANT ON PEUT UTILISER DF
    df['total_vente'] = df['prix'] * df['quantite']
    
    # Encodage (on utilise les colonnes de TA base : teint, type_peau, age, saison)
    for col in ['teint', 'type_peau', 'age', 'saison']:
        le = LabelEncoder()
        df[f'{col}_n'] = le.fit_transform(df[col].astype(str))

    # Entraînement
    X = df[['teint_n', 'type_peau_n', 'age_n', 'saison_n']]
    y = df['total_vente']

    model = LinearRegression()
    model.fit(X, y)

    # Prédiction test
    prediction = model.predict([[0, 0, 0, 0]])
    return round(float(prediction[0]), 2)