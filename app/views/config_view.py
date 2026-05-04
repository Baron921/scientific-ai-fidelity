import streamlit as st
from components.header import afficher_header


def afficher_config():
    afficher_header(
        titre="Configuration du dashboard",
        icone="",
        description="Activez ou désactivez les métriques que vous souhaitez analyser dans les différentes rubriques"
    )

    toutes_semantiques = ["BertScore", "BartScore", "Cos_Sim"]
    toutes_factuelles = ["FactCC", "FactAcc", "DAE", "FactScore", "NLI", "Cosine", "NaiveMatch", "BertScore",
                         "BartScore"]

    if 'filtre_semantique' not in st.session_state:
        st.session_state.filtre_semantique = toutes_semantiques.copy()

    if 'filtre_factuel' not in st.session_state:
        st.session_state.filtre_factuel = toutes_factuelles.copy()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Qualité sémantique")
        nouveau_filtre_semantique = []

        for metrique in toutes_semantiques:
            etat_actuel = metrique in st.session_state.filtre_semantique

            est_coche = st.toggle(metrique, value=etat_actuel, key=f"sem_{metrique}")

            if est_coche != etat_actuel:
                if est_coche:
                    st.toast(f"✅ **{metrique}** activé !", icon="")
                else:
                    st.toast(f"❌ **{metrique}** désactivé et masqué.", icon="")

            if est_coche:
                nouveau_filtre_semantique.append(metrique)

        st.session_state.filtre_semantique = nouveau_filtre_semantique

    with col2:
        st.subheader("Fidélité Factuelle")
        nouveau_filtre_factuel = []

        for metrique in toutes_factuelles:
            etat_actuel = metrique in st.session_state.filtre_factuel

            est_coche = st.toggle(metrique, value=etat_actuel, key=f"fac_{metrique}")

            if est_coche != etat_actuel:
                if est_coche:
                    st.toast(f"✅ **{metrique}** activé !")
                else:
                    st.toast(f"❌ **{metrique}** désactivé et masqué.")

            if est_coche:
                nouveau_filtre_factuel.append(metrique)

        st.session_state.filtre_factuel = nouveau_filtre_factuel

    st.divider()
    st.success("✅ Vos préférences sont sauvegardées automatiquement en temps réel.")