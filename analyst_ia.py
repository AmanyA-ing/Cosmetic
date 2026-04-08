import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder

# 1. Connexion à la base de données
engine = create_engine("sqlite:///./cosmetique.db")

def analyser_mes_ventes():
    # 2. On aspire les données SQL vers un DataFrame Pandas (Tableau intelligent)
    df = pd.read_sql("SELECT * FROM ventes", engine)

    if df.empty:
        print("La base est vide. Ajoute des ventes d'abord !")
        return

    #nettoyage
    df['teint'] = df['teint'].str.lower().str.strip()
    df['produit'] = df['produit'].str.lower().str.strip()

    print("--- 📊 ANALYSE CHRONO COSMETIC ---")
    
    # 3. Calcul du Chiffre d'Affaires (Prix * Quantité)
    df['total_ligne'] = df['prix'] * df['quantite']
    total_general = df['total_ligne'].sum()
    
    print(f"💰 Chiffre d'affaires total : {total_general} CFA")

    # 4. Analyse par Teint (Pour l'IA)
    # On regarde quel teint rapporte le plus
    stats_teint = df.groupby('teint')['total_ligne'].sum()
    print("\n📈 Ventes par type de teint :")
    print(stats_teint)

    # 5. Top Produit
    top_produit = df.groupby('produit')['quantite'].sum().idxmax()
    print(f"\n🏆 Produit le plus vendu : {top_produit}")

    # On sauvegarde une copie en Excel pour la cliente
    df.to_excel("rapport_ventes_ia.xlsx", index=False)
    print("\n✅ Rapport Excel 'rapport_ventes_ia.xlsx' généré !")

if __name__ == "__main__":
    analyser_mes_ventes()