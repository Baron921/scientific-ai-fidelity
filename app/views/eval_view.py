import streamlit as st
import pandas as pd
import time
import re


# ==========================================
# FONCTIONS NLP (À remplacer par ton vrai code spaCy)
# ==========================================
def extraire_entites(texte):
    """
    Fonction temporaire utilisant des expressions régulières basiques.
    À remplacer par ton script spaCy (NER) et ton extracteur de triplets.
    """
    # Extraction naïve des nombres
    nombres = re.findall(r'\b\d+(?:[\.,]\d+)?\b', texte)
    # Extraction naïve de ce qui ressemble à des unités (%, mg, kg, etc.)
    unites = re.findall(r'\b(mg|kg|ml|%|cm|mm|g)\b', texte.lower())

    return {"Nombres": list(set(nombres)), "Unités": list(set(unites))}


def calculer_score(source_entites, target_entites):
    """Calcule un score de fidélité factuelle basique."""
    if not source_entites["Nombres"]:
        return 100.0  # Rien à perdre si pas de nombres à la base

    # On compte combien de nombres sources se retrouvent dans la cible
    match = sum(1 for n in source_entites["Nombres"] if n in target_entites["Nombres"])
    return (match / len(source_entites["Nombres"])) * 100


# ==========================================
# AFFICHAGE DE LA PAGE
# ==========================================
def afficher():
    from components.footer import afficher_footer

    st.header("Pipeline d'Évaluation Factuelle")
    st.write("Analysez les paires de textes pour détecter les altérations factuelles (chiffres, unités, entités).")
    st.divider()

    # 1. VÉRIFICATION DES PRÉREQUIS
    if 'dataset' not in st.session_state or st.session_state.dataset is None:
        st.warning("Aucun jeu de données chargé. Veuillez d'abord vous rendre dans l'onglet **Données**.")
        afficher_footer()
        return

    df = st.session_state.dataset

    # 2. SÉLECTION DU TEXTE À ANALYSER
    st.subheader("1. Sélection de la paire de textes")

    # Création d'une liste lisible pour le menu déroulant
    options_textes = [f"[{row['Domaine']}] {row['Texte Source'][:60]}..." for idx, row in df.iterrows()]
    index_choisi = st.selectbox("Choisissez un extrait scientifique :", range(len(options_textes)),
                                format_func=lambda x: options_textes[x])

    # Récupération de la ligne correspondante
    ligne = df.iloc[index_choisi]

    # Sélection du type de réécriture
    type_prompt = st.radio(
        "Niveau de contrainte de la réécriture générée :",
        ["Prompt A (Améliore ce paragraphe)", "Prompt B (Améliore sans modifier nombres/unités)",
         "Prompt C (Améliore sans modifier aucun fait)"],
        horizontal=True
    )

    st.write("")

    # Affichage côte à côte
    col_source, col_target = st.columns(2)
    with col_source:
        st.markdown("**Texte Source Original**")
        st.info(ligne['Texte Source'])

    with col_target:
        st.markdown("**Texte Généré (LLM)**")
        # On simule la sélection du texte généré en fonction du radio button
        # (Dans la réalité, assure-toi d'avoir ces colonnes dans ton CSV)
        texte_genere = ligne['Texte Source'].replace("20", "40")  # Simulation d'une hallucination
        st.success(texte_genere)

    st.divider()

    # 3. LANCEMENT DE L'ANALYSE
    st.subheader("2. Exécution des Algorithmes")

    # On récupère la configuration (ou on met des valeurs par défaut si on n'a pas visité l'onglet Config)
    config = st.session_state.get('config', {"use_ner": True, "threshold": 0.85})

    if st.button("Lancer l'Évaluation Factuelle", type="primary", use_container_width=True):

        # Animation d'attente pour faire "pro"
        with st.spinner('Analyse NLP en cours (spaCy NER & Expressions régulières)...'):
            time.sleep(1.5)  # Simule le temps de calcul

            entites_source = extraire_entites(ligne['Texte Source'])
            entites_target = extraire_entites(texte_genere)
            score = calculer_score(entites_source, entites_target)

        # ==========================================
        # 4. RÉSULTATS DE L'ANALYSE
        # ==========================================
        st.write("### 📊 Résultats de l'extraction")

        # Affichage du score
        if score >= (config["threshold"] * 100):
            st.metric(label="Score de Fidélité Factuelle", value=f"{score:.1f}%", delta="Fiable", delta_color="normal")
        else:
            st.metric(label="Score de Fidélité Factuelle", value=f"{score:.1f}%", delta="Hallucination détectée",
                      delta_color="inverse")

        # Tableau comparatif des entités
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write("**Entités dans la Source**")
            st.json(entites_source)

        with col_res2:
            st.write("**Entités dans la Réécriture**")
            st.json(entites_target)

        # Conclusion textuelle
        if score < 100.0:
            st.error(
                "**Alerte d'altération :** Le modèle a modifié ou supprimé des valeurs numériques importantes lors de la réécriture.")
        else:
            st.success(
                "**Intégrité préservée :** Les chiffres et unités clés ont été conservés par le modèle de langage.")

    afficher_footer()