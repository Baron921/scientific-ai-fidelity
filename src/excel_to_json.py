import os.path

import pandas as pd
import json


def generer_json(fichier_excel, fichier_sortie, mode="imbrique"):
    try:
        all_sheets = pd.read_excel(fichier_excel, sheet_name=None)

        print("\nDébut de traitement de votre fichier ...")

        if mode == "imbrique":
            resultat = {}
        else:
            resultat = []

        for nom_onglet, df in all_sheets.items():

            # Nettoyage
            df = df.dropna(how='all')
            df = df.fillna("Non renseigné")
            df = df.apply(lambda col: col.astype(str).str.strip())
            df = df.replace(["-", ""], "Non renseigné")

            if mode == "simple":
                df['Domaine'] = nom_onglet.upper()

            records = df.to_dict(orient='records')

            if mode == "imbrique":
                resultat[nom_onglet.upper()] = records
                print(f" -> Onglet '{nom_onglet.upper()}' traité : {len(records)} articles.")
            else:
                resultat.extend(records)
                print(f" -> Onglet '{nom_onglet.upper()}' traité : {len(records)} articles ajoutés.")

        if not os.path.exists("data/json"):
            os.makedirs("data/json")

        fichier_sortie = os.path.join("data/json", fichier_sortie)
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            json.dump(resultat, f, indent=4, ensure_ascii=False)


        print(f"\nSUCCÈS ! Fichier {fichier_sortie} généré.")

    except FileNotFoundError:
        print(f"ERREUR : Le fichier {fichier_excel} est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


fichier_excel = "data/Catalogue des articles.xlsx"

print(f"Choisissez le type de JSON à générer :")
print("1 - JSON imbriqué (par domaine)")
print("2 - JSON simple (une seule liste)")
print("0 - Quitter")

choix = input("Votre choix (1 ou 2) : ").strip()

while choix not in ["0", "1", "2",]:
    choix = input("Veuillez choisir une option entre 1 ou 2 : ").strip()

if choix == "1":
    generer_json(fichier_excel, "dataset_imbrique.json", mode="imbrique")
elif choix == "2":
    generer_json(fichier_excel, "dataset_simple.json", mode="simple")
elif choix == "0":
    print("Programme quitté. À bientôt !")
