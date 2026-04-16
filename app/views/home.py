import streamlit as st
import os

from components.footer import afficher_footer

def afficher():
    # En-tête principal
    st.title("🔬 Évaluer la ﬁdélité factuelle des réécritures scientiﬁques générées par IA")
    st.markdown("### Détection d'hallucinations dans les réécritures scientifiques")

    st.divider()

    # Section de présentation
    col_texte, col_info = st.columns([2, 1])

    with col_texte:
        st.markdown("""
        **Bienvenue sur l'interface d'évaluation du projet TER (Master 1 ATAL).**

        Cette plateforme a été conçue pour analyser et comparer la fidélité factuelle 
        des textes scientifiques générés par des Modèles de Langage (LLM). 

        Contrairement aux métriques classiques (comme ROUGE ou BLEU) qui se concentrent 
        sur la syntaxe, notre approche vise à détecter les **hallucinations intrinsèques** en vérifiant strictement la préservation des entités clés :
        * Les valeurs numériques (chiffres, doses, pourcentages)
        * Les unités de mesure associées
        * Les relations logiques (Triplets : Sujet - Prédicat - Objet)
        """)

    with col_info:
        # Affichage de l'objectif sous forme de carte info
        st.info(
            "💡 **Objectif du Projet**\n\nProuver que l'extraction structurée (NER + Triplets) est plus fiable que la similarité de surface pour la validation scientifique.")

    st.markdown("---")

    # ==========================================
    # NOUVELLE SECTION : AFFICHAGE DU SCHÉMA
    # ==========================================
    st.subheader("📊 Pipeline de génération du jeu de données")
    st.write(
        "Le schéma ci-dessous illustre notre méthodologie pour générer les réécritures avec différents niveaux de contraintes factuelles (Prompting) :")

    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    # on remonte d'un cran pour aller à la racine du projet
    racine_projet = os.path.dirname(dossier_actuel)
    # on construit le chemin absolu vers l'image
    chemin_image = os.path.join(racine_projet, "assets", "TER_DRAW.png")

    try:
        st.image(chemin_image, caption="Méthodologie de réécriture avec contraintes via LLM", use_container_width=True)
    except FileNotFoundError:
        st.error(f"L'image est introuvable au chemin : {chemin_image}")
    st.markdown("---")

    # Guide d'utilisation en 3 étapes
    st.header("🚀 Comment utiliser cette plateforme ?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1. 📂 Données")
        st.write(
            "Commencez par importer votre jeu de données (fichier CSV) contenant les textes sources et les textes générés par l'IA.")
        st.caption("Allez dans l'onglet *Données*")

    with col2:
        st.markdown("### 2. ⚙️ Configuration")
        st.write(
            "Sélectionnez les algorithmes d'évaluation à activer (Baselines classiques vs Notre approche par extraction).")
        st.caption("Allez dans l'onglet *Configuration*")

    with col3:
        st.markdown("### 3. 🧪 Évaluation")
        st.write(
            "Lancez l'analyse sur une paire de textes spécifique pour visualiser la détection des erreurs en temps réel.")
        st.caption("Allez dans l'onglet *Évaluation*")

    st.markdown("---")

    # Pied de page
    # st.caption("👨‍💻 Projet réalisé sous la supervision de Pascal Molli | Équipe de recherche TER")

    afficher_footer()