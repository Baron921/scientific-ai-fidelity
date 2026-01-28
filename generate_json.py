import pandas as pd
import json

# ==========================================
# CONFIGURATION
# ==========================================
fichier_excel = "Catalogue des articles.xlsx"  # Remplacez par votre nom de fichier
fichier_sortie = "dataset_plat.json"

try:

    # sheet_name=None permet de charger toutes les feuilles dans un dictionnaire
    all_sheets = pd.read_excel(fichier_excel, sheet_name=None)

    liste_globale = []

    print("Début du traitement...")

    for nom_onglet, df in all_sheets.items():
        # Nettoyage : supprimer les lignes complètement vides
        df = df.dropna(how='all')

        # Sécurité : Convertir tout en texte pour éviter les erreurs de date (Timestamp) dans le JSON
        df = df.astype(str)

        # AJOUT DE L'INFORMATION DOMAINE
        # On crée une nouvelle colonne 'domaine' remplie avec le nom de l'onglet
        df['domaine'] = nom_onglet

        # Conversion de l'onglet en liste de dictionnaires
        records = df.to_dict(orient='records')

        # Ajout à la liste principale
        liste_globale.extend(records)
        print(f" -> Onglet '{nom_onglet}' traité : {len(records)} articles ajoutés.")

    # 2. Sauvegarde en JSON
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(liste_globale, f, indent=4, ensure_ascii=False)

    print(f"\nSUCCÈS ! Le fichier '{fichier_sortie}' a été créé avec {len(liste_globale)} articles au total.")

except FileNotFoundError:
    print(f"ERREUR : Le fichier '{fichier_excel}' est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")