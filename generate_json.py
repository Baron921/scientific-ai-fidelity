import pandas as pd
import json

fichier_excel = "Catalogue des articles.xlsx"
fichier_sortie = "dataset_plat.json"

try:

    all_sheets = pd.read_excel(fichier_excel, sheet_name=None)

    liste_globale = []

    print("Début de traitement du fichier ...")

    for nom_onglet, df in all_sheets.items():

        df = df.dropna(how='all')
        df = df.fillna("Non renseigné")
        df = df.apply(lambda col: col.astype(str).str.strip())
        df = df.replace(["-", ""], "Non renseigné")
        df['domaine'] = nom_onglet

        records = df.to_dict(orient='records')

        liste_globale.extend(records)
        print(f" -> Onglet {nom_onglet.upper()} traité : {len(records)} articles ajoutés.")

    # création et sauvegarde du fichier JSON
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(liste_globale, f, indent=4, ensure_ascii=False)

    print(f"\nSUCCÈS ! Le fichier {fichier_sortie} a été créé avec un total de {len(liste_globale)} articles")

except FileNotFoundError:
    print(f"ERREUR : Le fichier '{fichier_excel}' est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")