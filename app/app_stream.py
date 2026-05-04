import streamlit as st
import time
from streamlit_option_menu import option_menu

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="TER ATAL - Évaluation Factuelle",
    page_icon="🔬",
    layout="wide"
)

st.title("Évaluation de la fidélité factuelle des réécritures scientifiques générées par IA")
st.markdown("**Projet TER - Master 1 ATAL** | *Détection d'hallucinations dans les textes scientifiques*")

# ==========================================
# BARRE LATÉRALE : LE VRAI MENU
# ==========================================
with st.sidebar:
    st.markdown("### Navigation")
    selected = option_menu(
        menu_title=None,  # On masque le titre par défaut pour faire plus propre
        options=["Évaluation", "Configuration", "À propos"],
        icons=["play-circle", "sliders", "info-circle"],  # Icônes Bootstrap
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#007BFF", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#007BFF", "color": "white", "icon-color": "white"},
        }
    )

# Variables de configuration par défaut
use_rouge, use_scibert = True, True
use_ner, use_factacc = True, True
use_factcc, use_llm = True, True

# ==========================================
# PAGE : CONFIGURATION DU PIPELINE
# ==========================================
if selected == "Configuration":
    st.header("⚙️ Configuration du Pipeline d'Évaluation")
    st.write("Activez ou désactivez les métriques à inclure lors de l'analyse.")

    st.subheader("1. Baselines (Surface & Sémantique)")
    use_rouge = st.checkbox("ROUGE-1 & ROUGE-L", value=True)
    use_scibert = st.checkbox("SciBERTScore", value=True)

    st.subheader("2. Extraction Structurée (Notre Approche)")
    use_ner = st.checkbox("Préservation des Entités (NER)", value=True)
    use_factacc = st.checkbox("Précision Factuelle (fact_acc)", value=True)

    st.subheader("3. Modèles Avancés")
    use_factcc = st.checkbox("FactCC (NLI)", value=True)
    use_llm = st.checkbox("LLM-as-a-Judge (Analyse fine)", value=True)

# ==========================================
# PAGE : À PROPOS
# ==========================================
elif selected == "À propos":
    st.header("ℹ️ À propos du Projet TER")
    st.write(
        "Ce projet vise à détecter les hallucinations intrinsèques dans les textes scientifiques en se concentrant sur la préservation des entités nommées (chiffres, unités de mesure). L'approche repose sur l'extraction symbolique de triplets relationnels et la reconnaissance d'entités nommées (NER) pour vérifier l'intégrité des données.")

# ==========================================
# PAGE : ÉVALUATION (Page Principale)
# ==========================================
elif selected == "Évaluation":
    st.write("### Textes à analyser")

    col1, col2 = st.columns(2)
    with col1:
        source_text = st.text_area(
            "Paragraphe Source (Vérité Terrain)",
            value="Le patient a reçu une dose de 10 mg d'aspirine par jour pendant 4 semaines, ce qui a réduit la pression artérielle de 15%.",
            height=120
        )

    with col2:
        generated_text = st.text_area(
            "Réécriture générée par IA",
            value="Une dose quotidienne de 100 mg d'aspirine a été administrée au patient sur une période de 4 semaines, entraînant une baisse de 15% de la pression artérielle.",
            height=120
        )


    # --- DONNÉES STATIQUES (MOCKS) ---
    def get_static_baselines():
        return {"ROUGE-1": "0.89", "SciBERTScore": "0.94"}


    def get_static_ner_visualisation():
        html_result = """
        <div style="line-height: 1.6; font-size: 16px; background-color: #f9f9f9; padding: 15px; border-radius: 8px;">
            Une dose quotidienne de 
            <span style='background-color: #ffcccc; padding: 2px 4px; border-radius: 4px; color: #cc0000; border: 1px solid #cc0000;'>
                <b>100 mg ❌ (Source: 10 mg)</b>
            </span> 
            d'<span style='background-color: #e6f3ff; padding: 2px 4px; border-radius: 4px; color: #0066cc;'>aspirine</span> 
            a été administrée au patient sur une période de 
            <span style='background-color: #e6f3ff; padding: 2px 4px; border-radius: 4px; color: #0066cc;'>4 semaines</span>, 
            entraînant une baisse de 
            <span style='background-color: #e6f3ff; padding: 2px 4px; border-radius: 4px; color: #0066cc;'>15%</span> 
            de la pression artérielle.
        </div>
        """
        return html_result, "0.75"


    def get_static_fact_acc():
        return "0.66"


    # --- EXÉCUTION DU PIPELINE ---
    if st.button("Lancer l'Évaluation Factuelle", type="primary"):
        st.divider()
        st.write("### Résultats de l'analyse")

        progress_text = "Analyse en cours..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.3)
        my_bar.empty()

        if use_rouge or use_scibert:
            st.markdown("#### 1. Métriques Classiques (Le Faux Positif)")
            st.info(
                "💡 *Note : Ces métriques donnent un score très élevé car la similarité syntaxique est forte, masquant l'erreur médicale grave.*")
            res_baselines = get_static_baselines()
            b_col1, b_col2, b_col3 = st.columns(3)
            if use_rouge:
                b_col1.metric("ROUGE-1", res_baselines["ROUGE-1"], delta="Score élevé (Trompeur)", delta_color="off")
            if use_scibert:
                b_col2.metric("SciBERTScore", res_baselines["SciBERTScore"], delta="Très élevé", delta_color="off")

        if use_ner or use_factacc:
            st.markdown("---")
            st.markdown("#### 2. Extraction Structurée (Notre Méthode)")
            n_col1, n_col2 = st.columns([1, 2])

            if use_factacc:
                score_factacc = get_static_fact_acc()
                n_col1.metric("Factual Accuracy (fact_acc)", score_factacc, delta="-0.34 (Altération logique)",
                              delta_color="inverse")

            if use_ner:
                html_visu, score_ner = get_static_ner_visualisation()
                n_col1.metric("Préservation des Entités", score_ner, delta="1 erreur critique", delta_color="inverse")
                with n_col2:
                    st.write("**Visualisation des Hallucinations Numériques (NER) :**")
                    st.markdown(html_visu, unsafe_allow_html=True)

        if use_factcc or use_llm:
            st.markdown("---")
            st.markdown("#### 3. Analyse Neuronale et Logique")
            if use_factcc:
                st.error(
                    "🚨 **FactCC (NLI) : INCOHÉRENCE DÉTECTÉE** \n\nLe modèle identifie une contradiction factuelle formelle entre la source et la génération.")
            if use_llm:
                st.warning(
                    "⚖️ **LLM-as-a-Judge (Analyse Oracle) :** \n\nLe texte est grammaticalement parfait. Cependant, il présente une **hallucination intrinsèque sévère** : la valeur numérique de la dose a été multipliée par 10 (100 mg au lieu de 10 mg), ce qui altère totalement la validité du résultat clinique.")