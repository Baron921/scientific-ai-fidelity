import pandas as pd
import json

fichier_excel = "Catalogue des articles.xlsx"  # Remplacez par votre nom de fichier
fichier_sortie = "dataset_imbrique.json"

try:
    all_sheets = pd.read_excel(fichier_excel, sheet_name=None)

    dictionnaire_final = {}
    print(dictionnaire_final)
    print("Début du traitement...")

    for nom_onglet, df in all_sheets.items():

        df = df.dropna(how='all')
        df = df.fillna("Non renseigné")
        df = df.apply(lambda col: col.astype(str).str.strip())
        df = df.replace(["-", ""], "Non renseigné")
        records = df.to_dict(orient='records')
        dictionnaire_final[nom_onglet.upper()] = records

        print(f" -> Onglet '{nom_onglet}' traité : {len(records)} articles.")

    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(dictionnaire_final, f, indent=4, ensure_ascii=False)

    print(f"\nSUCCÈS ! Le fichier {fichier_sortie} a été créé avec {len(dictionnaire_final)} domaines.")

except FileNotFoundError:
    print(f"ERREUR : Le fichier '{fichier_excel}' est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")