import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

engine = create_engine("sqlite:///./cosmetique.db")

def predire_produit(teint, peau, age, saison, event):
    try:
        df = pd.read_sql("SELECT * FROM ventes", engine)
    except:
        return "Pas de base de données"

    if len(df) < 2: 
        return "Besoin de plus de ventes"

    # Encodage du produit
    le_prod = LabelEncoder()
    df['produit_n'] = le_prod.fit_transform(df['produit'])
    
    # On utilise les VRAIS noms de ta base : age, type_peau, saison
    for col in ['teint', 'type_peau', 'age', 'saison']:
        le = LabelEncoder()
        df[f'{col}_n'] = le.fit_transform(df[col].astype(str))

    # Entraînement sur les colonnes existantes
    X = df[['teint_n', 'type_peau_n', 'age_n', 'saison_n']]
    y = df['produit_n']
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    # Prédiction rapide
    prediction = model.predict([[0, 0, 0, 0]]) 
    return le_prod.inverse_transform(prediction)[0]