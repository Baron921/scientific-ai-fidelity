import pandas as pd
import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from components.header import afficher_header
from components.footer import afficher_footer

# ==========================================
# FONCTION DE CHARGEMENT DES DONNÉES
# ==========================================
@st.cache_data
def format_data():
    """Charge via le module global et formate le JSON en DataFrame Pandas."""

    raw_data = load_data("dataset_imbrique.json")

    if raw_data is None:
        return None

    flat_list = []

    for domain, items in raw_data.items():
        for item in items:
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

def afficher():
    afficher_header(
        titre="Exploration du jeu de données",
        icone="",
        description="Ce jeu de données a été constitué pour évaluer la fidélité factuelle des réécritures. Il contient 121 passages scientifiques issus de la littérature académique, riches en entités numériques et nommées"
    )

    # st.divider()

    # chargement des données
    df = format_data()

    if df is None:
        st.error("Impossible de trouver le fichier `dataset_imbrique.json` dans le dossier `assets/`.")
        afficher_footer()
        return

    st.session_state.dataset = df

    st.subheader("Vue d'ensemble")
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
    st.subheader("Répartition du corpus")

    repartition = df["Domaine"].value_counts().reset_index()
    repartition.columns = ["Domaine", "Nombre de textes"]

    fig = px.pie(
        repartition,
        names="Domaine",
        values="Nombre de textes",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Textes: %{value}<extra></extra>"
    )

    fig.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        showlegend=False,
        height=350
    )

    col_vide1, col_graph, col_vide2 = st.columns([1, 2, 1])
    with col_graph:
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Explorer les textes")

    domaines_disponibles = ["Tous les domaines"] + list(df["Domaine"].unique())
    domaine_choisi = st.selectbox("Filtrer par domaine :", domaines_disponibles)

    if domaine_choisi == "Tous les domaines":
        df_filtre = df
    else:
        df_filtre = df[df["Domaine"] == domaine_choisi]

    st.write(f"Affichage de **{len(df_filtre)}** publications :")

    # st.dataframe permet un affichage interactif (tri, redimensionnement)
    st.dataframe(
        df_filtre[["Domaine", "Date", "Auteur", "Texte Source", "DOI"]],
        use_container_width=True,
        hide_index=True,
        height=400
    )

    st.info(
        "**Note pour l'évaluation :** Les textes sources de ce tableau seront utilisés comme vérité terrain dans notre pipeline NLP situé dans l'onglet **Évaluation**.")

    afficher_footer()