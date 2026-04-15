import streamlit as st
import time

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="TER ATAL - Évaluation Factuelle",
    page_icon="🔬",
    layout="wide"
)

st.title("Évaluation de la fidélité factuelle des réécritures scientiﬁques générées par IA")
st.markdown("**Projet TER - Master 1 ATAL** | *Détection d'hallucinations dans les textes scientifiques*")

# ==========================================
# BARRE LATÉRALE
# ==========================================
st.sidebar.header("Configuration du Pipeline")

st.sidebar.subheader("1. Baselines (Surface & Sémantique)")
use_rouge = st.sidebar.checkbox("ROUGE-1 & ROUGE-L", value=True)
use_scibert = st.sidebar.checkbox("SciBERTScore", value=True)

st.sidebar.subheader("2. Extraction Structurée (Notre Approche)")
use_ner = st.sidebar.checkbox("Préservation des Entités (NER)", value=True)
use_factacc = st.sidebar.checkbox("Précision Factuelle (fact_acc)", value=True)

st.sidebar.subheader("3. Modèles Avancés")
use_factcc = st.sidebar.checkbox("FactCC (NLI)", value=True)
use_llm = st.sidebar.checkbox("LLM-as-a-Judge (Analyse fine)", value=True)

# ==========================================
# INTERFACE UTILISATEUR (INPUTS)
# ==========================================
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


# ==========================================
# DONNÉES STATIQUES (MOCKS POUR TESTER L'UI)
# ==========================================
def get_static_baselines():
    # Des scores très hauts pour prouver que les baselines se font "piéger" par la syntaxe
    return {"ROUGE-1": "0.89", "SciBERTScore": "0.94"}


def get_static_ner_visualisation():
    # Rendu HTML simulant la détection des entités (Vert = OK, Rouge = Hallucination)
    html_result = """
    <div style="line-height: 1.6; font-size: 16px;">
        Une dose quotidienne de 
        <span style='background-color: #ffcccc; padding: 2px 4px; border-radius: 4px; color: #cc0000; border: 1px solid #cc0000;'>
            <b>100 mg️ (Source: 10 mg)</b>
        </span> 
        d'<span style='background-color: #e6f3ff; padding: 2px 4px; border-radius: 4px; color: #0066cc;'>aspirine</span> 
        a été administrée au patient sur une période de 
        <span style='background-color: #e6f3ff; padding: 2px 4px; border-radius: 4px; color: #0066cc;'>4 semaines</span>, 
        entraînant une baisse de 
        <span style='background-color: #e6f3ff; padding: 2px 4px; border-radius: 4px; color: #0066cc;'>15%</span> 
        de la pression artérielle.
    </div>
    """
    return html_result, "0.75"  # 3 entités correctes sur 4


def get_static_fact_acc():
    # Précision factuelle basée sur les triplets (Sujet, Relation, Objet)
    return "0.66"


# ==========================================
# EXÉCUTION DU PIPELINE ET AFFICHAGE
# ==========================================
if st.button("Lancer l'Évaluation Factuelle", type="primary"):

    st.divider()
    st.write("### Résultats de l'analyse")

    # Barre de progression simulée pour l'effet UX
    progress_text = "Analyse en cours..."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.5)
    my_bar.empty()

    # --- Section 1: Baselines ---
    if use_rouge or use_scibert:
        st.markdown("#### 1. Métriques Classiques (Le Faux Positif)")
        st.info(
            " *Note : Ces métriques donnent un score très élevé car la similarité des mots est forte, masquant l'erreur médicale grave (100mg au lieu de 10mg).*")

        res_baselines = get_static_baselines()
        b_col1, b_col2, b_col3 = st.columns(3)
        if use_rouge:
            b_col1.metric("ROUGE-1", res_baselines["ROUGE-1"], delta="Score élevé (Trompeur)", delta_color="off")
        if use_scibert:
            b_col2.metric("SciBERTScore", res_baselines["SciBERTScore"], delta="Très Élevé", delta_color="off")

    # --- Section 2: Ton Approche (NER & fact_acc) ---
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

    # --- Section 3: Modèles Avancés ---
    if use_factcc or use_llm:
        st.markdown("---")
        st.markdown("#### 3. Analyse Neuronale et Logique")

        if use_factcc:
            st.error(
                " **FactCC (NLI) : INCOHÉRENCE DÉTECTÉE** \n\nLe modèle identifie une contradiction factuelle formelle entre la source et la génération.")
        if use_llm:
            st.warning(
                "**LLM-as-a-Judge (Analyse Oracle) :** \n\nLe texte est grammaticalement parfait et respecte le ton scientifique. Cependant, il présente une **hallucination intrinsèque sévère** : la valeur numérique de la dose d'aspirine a été multipliée par 10 (100 mg au lieu de 10 mg), ce qui altère totalement la validité du résultat clinique.")