import pandas as pd
import json

# ==========================================
# CONFIGURATION
# ==========================================
fichier_excel = "Catalogue des articles.xlsx"  # Remplacez par votre nom de fichier
fichier_sortie = "dataset_imbrique.json"

# ==========================================
# SCRIPT
# ==========================================
try:
    all_sheets = pd.read_excel(fichier_excel, sheet_name=None)

    dictionnaire_final = {}

    print("Début du traitement...")

    for nom_onglet, df in all_sheets.items():
        # Nettoyage
        df = df.dropna(how='all')

        # Sécurité : Convertir tout en texte (dates, chiffres)
        df = df.astype(str)

        # Note : Ici, on n'ajoute PAS la colonne 'domaine' dans les données,
        # car l'information est déjà dans la clé du dictionnaire parent.

        # Conversion
        records = df.to_dict(orient='records')

        # INSERTION DANS LE DICTIONNAIRE
        # La clé est le nom de l'onglet, la valeur est la liste des articles
        dictionnaire_final[nom_onglet] = records

        print(f" -> Onglet '{nom_onglet}' traité : {len(records)} articles.")

    # 2. Sauvegarde
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(dictionnaire_final, f, indent=4, ensure_ascii=False)

    print(f"\nSUCCÈS ! Le fichier '{fichier_sortie}' a été créé avec {len(dictionnaire_final)} domaines.")

except FileNotFoundError:
    print(f"ERREUR : Le fichier '{fichier_excel}' est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")