import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px


# ==========================================
# FONCTION DE CHARGEMENT DES DONNÉES
# ==========================================
@st.cache_data
def load_data():
    """Charge et nettoie le fichier JSON en gérant les chemins de manière robuste."""
    # Calcul du chemin absolu vers le fichier JSON
    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_actuel)
    chemin_json = os.path.join(racine_projet, "../json", "dataset_imbrique.json")

    try:
        with open(chemin_json, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        flat_list = []
        # On parcourt chaque domaine et ses éléments
        for domain, items in raw_data.items():
            for item in items:
                # Gestion des petites incohérences de nommage dans le JSON
                texte = item.get("Paragraphes", item.get("Paragraphe", "Non renseigné"))
                url = item.get("URL", item.get("URL / PDF", "Non renseigné"))

                flat_list.append({
                    "Domaine": domain,
                    "Date": item.get("Date de publication", "Non renseigné"),
                    "Auteur": item.get("Auteur", "Non renseigné"),
                    "DOI": item.get("Doi", "Non renseigné"),
                    "Texte Source": texte,
                    "URL": url,
                    "Licence": item.get("Licence", "Non renseigné")
                })
        return pd.DataFrame(flat_list)
    except FileNotFoundError:
        return None


# ==========================================
# AFFICHAGE DE LA PAGE
# ==========================================
def afficher():
    from components.footer import afficher_footer

    st.header("📂 Exploration du Dataset")
    st.write(
        "Ce jeu de données a été constitué pour évaluer la fidélité factuelle des réécritures. Il contient 100 passages scientifiques issus de la littérature académique, riches en entités numériques et nommées.")

    st.divider()

    # Chargement des données
    df = load_data()

    if df is None:
        st.error("⚠️ Impossible de trouver le fichier `dataset_imbrique.json` dans le dossier `assets/`.")
        afficher_footer()
        return

    # On sauvegarde le dataset dans la mémoire globale pour l'utiliser dans l'onglet Évaluation
    st.session_state.dataset = df

    # ==========================================
    # 1. MÉTRIQUES GLOBALES (KPIs)
    # ==========================================
    st.subheader("📊 Vue d'ensemble")
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric(label="Total des paragraphes", value=len(df))
    with col2:
        with st.container(border=True):
            st.metric(label="Domaines scientifiques", value=df["Domaine"].nunique())
    with col3:
        with st.container(border=True):
            st.metric(label="Licence globale", value="CC BY 4.0")

    st.write("")

    # col1, col2, col3 = st.columns(3)
    #
    # # Style CSS réutilisable pour tes cartes
    # card_style = """
    # <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center;">
    #     <h4 style="margin: 0; color: #555; font-size: 14px; font-weight: normal;">{label}</h4>
    #     <h2 style="margin: 5px 0 0 0; color: #1E88E5; font-size: 28px;">{value}</h2>
    # </div>
    # """
    #
    # with col1:
    #     st.markdown(card_style.format(label="Total des paragraphes", value=len(df)), unsafe_allow_html=True)
    # with col2:
    #     st.markdown(card_style.format(label="Domaines scientifiques", value=df["Domaine"].nunique()),
    #                 unsafe_allow_html=True)
    # with col3:
    #     st.markdown(card_style.format(label="Licence globale", value="CC BY 4.0"), unsafe_allow_html=True)

    # ==========================================
    # 2. RÉPARTITION VISUELLE
    # ==========================================
    # ==========================================
    # 2. RÉPARTITION VISUELLE (Donut Chart)
    # ==========================================
    st.subheader("📊 Répartition du corpus")

    # On transforme les données pour Plotly
    repartition = df["Domaine"].value_counts().reset_index()
    repartition.columns = ["Domaine", "Nombre de textes"]

    # Création du graphique en Anneau (Donut)
    fig = px.pie(
        repartition,
        names="Domaine",
        values="Nombre de textes",
        hole=0.45,  # Taille du trou au centre (effet Donut)
        color_discrete_sequence=px.colors.qualitative.Pastel  # Couleurs douces et modernes
    )

    # Personnalisation du design
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',  # Affiche le nom du domaine et le pourcentage (20%)
        hovertemplate="<b>%{label}</b><br>Textes: %{value}<extra></extra>"  # Info au survol
    )

    # On enlève les marges pour que ça s'intègre bien dans la page
    fig.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        showlegend=False,  # On cache la légende sur le côté car les noms sont sur le graphique
        height=350
    )

    # Affichage sur Streamlit
    col_vide1, col_graph, col_vide2 = st.columns([1, 2, 1])
    with col_graph:
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================
    # 3. EXPLORATEUR INTERACTIF
    # ==========================================
    st.subheader("🔍 Explorer les textes")

    # Filtre par domaine
    domaines_disponibles = ["Tous les domaines"] + list(df["Domaine"].unique())
    domaine_choisi = st.selectbox("Filtrer par domaine :", domaines_disponibles)

    # Application du filtre
    if domaine_choisi == "Tous les domaines":
        df_filtre = df
    else:
        df_filtre = df[df["Domaine"] == domaine_choisi]

    # Affichage du tableau interactif
    st.write(f"Affichage de **{len(df_filtre)}** publications :")

    # st.dataframe permet un affichage interactif (tri, redimensionnement)
    st.dataframe(
        df_filtre[["Domaine", "Date", "Auteur", "Texte Source", "DOI"]],
        use_container_width=True,
        hide_index=True,
        height=400
    )

    st.info(
        "💡 **Note pour l'évaluation :** Les textes sources de ce tableau seront utilisés comme vérité terrain dans notre pipeline NLP situé dans l'onglet **Évaluation**.")

    afficher_footer()