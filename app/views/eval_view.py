import pandas as pd
import streamlit as st
import plotly.express as px
from collections import defaultdict

from components.header import afficher_header
from utils.data_loader import load_data
import streamlit.components.v1 as components
from components.footer import afficher_footer

# ==========================================
# FONCTIONS DE TRAITEMENT (Mises en cache)
# ==========================================
@st.cache_data
def generer_statistiques(data):
    """Calcule les statistiques dynamiquement, et prépare les données pour le tableau de l'article."""
    total_articles = sum(len(articles) for articles in data.values())

    stats_prompts = {
        "Rew1": {"erreurs": 0, "suppressions": 0, "ajouts": 0},
        "Rew2": {"erreurs": 0, "suppressions": 0, "ajouts": 0},
        "Rew3": {"erreurs": 0, "suppressions": 0, "ajouts": 0}
    }

    stats_categories = defaultdict(lambda: {"suppressions": 0, "ajouts": 0, "total": 0})

    table_erreurs_par_prompt = defaultdict(lambda: {"Rew1": 0, "Rew2": 0, "Rew3": 0})
    textes_hallucines = {"Rew1": 0, "Rew2": 0, "Rew3": 0}

    records_details = []

    for domaine, articles in data.items():
        for article in articles:
            evaluations = article.get("Evaluations", {})
            for prompt in ["Rew1", "Rew2", "Rew3"]:
                if prompt in evaluations:
                    rapport = evaluations[prompt]
                    total_err = rapport.get("total_erreurs", 0)

                    stats_prompts[prompt]["erreurs"] += total_err

                    if total_err > 0:
                        textes_hallucines[prompt] += 1

                    sup_totales = 0
                    add_totales = 0

                    details = rapport.get("details", {})
                    for cat, dict_erreurs in details.items():
                        sup = len(dict_erreurs.get("suppressions", []))
                        add = len(dict_erreurs.get("ajouts", []))
                        erreurs_cat = sup + add

                        sup_totales += sup
                        add_totales += add

                        stats_categories[cat]["suppressions"] += sup
                        stats_categories[cat]["ajouts"] += add
                        stats_categories[cat]["total"] += erreurs_cat

                        table_erreurs_par_prompt[cat][prompt] += erreurs_cat

                    stats_prompts[prompt]["suppressions"] += sup_totales
                    stats_prompts[prompt]["ajouts"] += add_totales

                    records_details.append({
                        "Domaine": domaine,
                        "Prompt": prompt,
                        "Total Erreurs": total_err,
                        "Suppressions": sup_totales,
                        "Ajouts": add_totales
                    })

    df_details = pd.DataFrame(records_details)

    return total_articles, stats_prompts, dict(stats_categories), df_details, dict(
        table_erreurs_par_prompt), textes_hallucines


# ==========================================
# FONCTION PRINCIPALE D'AFFICHAGE
# ==========================================
def afficher():
    afficher_header(
        titre="Name Entity Recognition (NER)",
        icone="",
        description="Analysez la fidélité factuelle des réécritures et visualisez la distribution des hallucinations"
    )
    # 1. CHARGEMENT DES DONNÉES
    nom_du_fichier = "resultats_complets_ner_new.json"
    data = load_data(nom_du_fichier)

    # 2. AFFICHAGE DU DASHBOARD
    if data is not None:
        st.session_state.dataset = data
        total_articles, stats_prompts, stats_categories, df_details, table_erreurs_par_prompt, textes_hallucines = generer_statistiques(
            data)

        df_domaine_prompt = df_details.groupby(['Domaine', 'Prompt'])[
            ['Suppressions', 'Ajouts', 'Total Erreurs']].sum().reset_index()


        # st.header("")

        total_reecritures = len(df_details)

        html_cards = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
                    body {{
                        margin: 0;
                        padding: 10px 5px;
                        font-family: 'Source Sans Pro', sans-serif;
                        background-color: transparent;
                    }}
                    .container {{
                        display: flex;
                        gap: 1rem;
                        justify-content: space-between;
                    }}
                    .card {{
                        flex: 1;
                        background-color: white;
                        padding: 15px 15px;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        border: 1px solid #f0f2f6;
                    }}
                    .card-title {{
                        font-size: 13px;
                        color: #6c757d;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        display: flex;
                        align-items: center;
                        gap: 6px;
                    }}
                    .material-symbols-outlined {{
                        font-size: 15px;
                    }}
                    .card-value {{
                        font-size: 26px;
                        color: #212529;
                        font-weight: bold;
                        margin-top: 5px;
                    }}
                </style>
                </head>
                <body>
                    <div class="container">
                        <div class="card" style="border-left: 5px solid #007BFF;">
                            <div class="card-title">
                                <span class="material-symbols-outlined">article</span> Textes Sources
                            </div>
                            <div class="card-value" data-target="{total_articles}">0</div>
                        </div>
                        <div class="card" style="border-left: 5px solid #9b59b6;">
                            <div class="card-title">
                                <span class="material-symbols-outlined">edit_note</span> Réécritures
                            </div>
                            <div class="card-value" data-target="{total_reecritures}">0</div>
                        </div>
                        <div class="card" style="border-left: 5px solid #e74c3c;">
                            <div class="card-title">
                                <span class="material-symbols-outlined">bug_report</span> Erreurs Rew1
                            </div>
                            <div class="card-value" data-target="{stats_prompts['Rew1']['erreurs']}">0</div>
                        </div>
                        <div class="card" style="border-left: 5px solid #f39c12;">
                            <div class="card-title">
                                <span class="material-symbols-outlined">bug_report</span> Erreurs Rew2
                            </div>
                            <div class="card-value" data-target="{stats_prompts['Rew2']['erreurs']}">0</div>
                        </div>
                        <div class="card" style="border-left: 5px solid #2ecc71;">
                            <div class="card-title">
                                <span class="material-symbols-outlined">bug_report</span> Erreurs Rew3
                            </div>
                            <div class="card-value" data-target="{stats_prompts['Rew3']['erreurs']}">0</div>
                        </div>
                    </div>

                    <script>
                        const counters = document.querySelectorAll('.card-value');
                        const speed = 40; 

                        counters.forEach(counter => {{
                            const updateCount = () => {{
                                const target = +counter.getAttribute('data-target');
                                const count = +counter.innerText;
                                const inc = target / speed;

                                if (count < target) {{
                                    counter.innerText = Math.ceil(count + inc);
                                    setTimeout(updateCount, 30); 
                                }} else {{
                                    counter.innerText = target;
                                }}
                            }};
                            updateCount();
                        }});
                    </script>
                </body>
                </html>
                """

        components.html(html_cards, height=120)

        st.markdown("### Bilan : Distribution et Tableau Synthétique")
        st.divider()
        tab_table, tab_dist = st.tabs(["Tableau", "Distribution par domaine"])

        with tab_table:
            traduction_cat = {
                "Noms_Propres": "Proper Nouns",
                "Mesures": "Measurements",
                "References": "References",
                "Molecules_Chimiques": "Chemical Molecules",
                "Equations": "Equations",
                "Nombres": "Numbers",
                "Montants": "Amounts",
                "Formules_Inline": "Formulas"
            }

            lignes_tableau = []
            for cat, scores in table_erreurs_par_prompt.items():
                lignes_tableau.append({
                    "Metrics & Error Types": traduction_cat.get(cat, cat.replace('_', ' ')),
                    "Variant 1": scores["Rew1"],
                    "Variant 2": scores["Rew2"],
                    "Variant 3": scores["Rew3"]
                })
            df_lignes = pd.DataFrame(lignes_tableau)

            df_total = pd.DataFrame([{
                "Metrics & Error Types": "Total Factual Errors",
                "Variant 1": df_lignes["Variant 1"].sum(),
                "Variant 2": df_lignes["Variant 2"].sum(),
                "Variant 3": df_lignes["Variant 3"].sum()
            }])

            taux_v1 = (textes_hallucines["Rew1"] / total_articles) * 100 if total_articles > 0 else 0
            taux_v2 = (textes_hallucines["Rew2"] / total_articles) * 100 if total_articles > 0 else 0
            taux_v3 = (textes_hallucines["Rew3"] / total_articles) * 100 if total_articles > 0 else 0

            df_halluc = pd.DataFrame([
                {
                    "Metrics & Error Types": "Hallucinated Texts",
                    "Variant 1": textes_hallucines["Rew1"],
                    "Variant 2": textes_hallucines["Rew2"],
                    "Variant 3": textes_hallucines["Rew3"]
                },
                {
                    "Metrics & Error Types": "Hallucination Rate (%)",
                    "Variant 1": f"{taux_v1:.2f}",
                    "Variant 2": f"{taux_v2:.2f}",
                    "Variant 3": f"{taux_v3:.2f}"
                }
            ])

            df_article = pd.concat([df_lignes, df_total, df_halluc], ignore_index=True)
            df_article.set_index("Metrics & Error Types", inplace=True)

            st.table(df_article)

        with tab_dist:
            fig3 = px.bar(
                df_domaine_prompt,
                x='Domaine',
                y='Total Erreurs',
                color='Prompt',
                barmode='group',
                labels={'Total Erreurs': "Nombre total d'altérations"},
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig3.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig3, use_container_width=True)

        # --- PARTIE 2 : GRAPHIQUES ---
        st.subheader("Analyses visuelles des altérations")
        st.divider()
        col_graph1, col_graph2 = st.columns(2)

        with col_graph1:
            st.markdown("##### Oublis vs Hallucinations (par modèle)")
            df_global_prompt = df_details.groupby('Prompt')[['Suppressions', 'Ajouts']].sum().reset_index()
            fig1 = px.bar(
                df_global_prompt,
                x='Prompt',
                y=['Suppressions', 'Ajouts'],
                barmode='group',
                labels={'value': "Nombre d'occurrences", 'variable': "Type d'altération"},
                color_discrete_map={"Suppressions": "#e74c3c", "Ajouts": "#f39c12"}
            )
            fig1.update_layout(margin=dict(l=0, r=0, t=30, b=0), legend_title_text='')
            st.plotly_chart(fig1, use_container_width=True)

        with col_graph2:
            st.markdown("##### Heatmap des Erreurs (Domaine vs Prompt)")
            df_pivot = df_domaine_prompt.pivot(index='Domaine', columns='Prompt', values='Total Erreurs').fillna(0)
            fig2 = px.imshow(
                df_pivot,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='Reds',
                labels=dict(x="Modèle (Prompt)", y="Domaine Scientifique", color="Total Erreurs")
            )
            fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig2, use_container_width=True)


        st.subheader("Explorateur d'altérations du pipeline NER")
        st.divider()
        col_dom, col_art, col_prm = st.columns([1, 2, 1])
        domaine_choisi = col_dom.selectbox("Domaines", list(data.keys()))
        articles_domaine = data[domaine_choisi]

        liste_titres = [f"Article {i + 1} (DOI: {a.get('DOI', 'N/A')})" for i, a in enumerate(articles_domaine)]
        article_idx = col_art.selectbox("Articles", range(len(liste_titres)),
                                        format_func=lambda x: liste_titres[x])
        prompt_choisi = col_prm.radio("Réécritures", ["Rew1", "Rew2", "Rew3"], horizontal=True)

        article_choisi = articles_domaine[article_idx]
        eval_data = article_choisi.get("Evaluations", {}).get(prompt_choisi, {})

        c_source, c_gen = st.columns(2)

        with c_source:
            st.info("**Texte source**")
            with st.container(height=400):
                # On récupère le texte
                texte_original = article_choisi.get("Texte_Source", article_choisi.get("Texte_source", ""))
                st.markdown(f"<div style='text-align: justify;'>{texte_original}</div>", unsafe_allow_html=True)

        with c_gen:
            st.success(f"**Réécriture par le LLM ({prompt_choisi})**")
            with st.container(height=400):
                texte_genere = eval_data.get("texte_evalue", "Texte non trouvé ou non évalué.")
                st.markdown(f"<div style='text-align: justify;'>{texte_genere}</div>", unsafe_allow_html=True)
        st.text("Détail de l'extraction algorithmique")

        if not eval_data:
            st.warning("Aucune donnée d'évaluation trouvée.", icon=":material/warning:")
        elif eval_data.get("total_erreurs", 0) == 0:
            st.success("Fidélité factuelle de 100% validée par le pipeline.", icon=":material/verified:")
        else:
            st.error(f"{eval_data['total_erreurs']} erreurs détectées.", icon=":material/error:")

            details = eval_data.get("details", {})
            if details:
                onglets = st.tabs([cat.replace("_", " ") for cat in details.keys()])
                for i, cat in enumerate(details.keys()):
                    with onglets[i]:
                        erreurs_cat = details.get(cat, {})
                        suppressions = erreurs_cat.get("suppressions", [])
                        ajouts = erreurs_cat.get("ajouts", [])

                        c_sup, c_add = st.columns(2)

                        with c_sup:
                            st.markdown("#### :material/do_not_disturb_on: Suppressions")
                            if suppressions:
                                html_sup = ""
                                for s in suppressions:
                                    html_sup += f"""
                                                            <div style="
                                                                display: inline-block;
                                                                background-color: #fadbd8; 
                                                                border-left: 4px solid #e74c3c; 
                                                                padding: 6px 12px; 
                                                                border-radius: 4px; 
                                                                margin: 0px 8px 8px 0px; 
                                                                color: #78281f; 
                                                                font-weight: 500;
                                                                font-size: 14px;
                                                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                                            ">
                                                                {s}
                                                            </div>
                                                            """
                                st.markdown(html_sup, unsafe_allow_html=True)
                            else:
                                st.write("Aucun oubli")

                        with c_add:
                            st.markdown("#### :material/add_circle: Ajouts")
                            if ajouts:
                                html_add = ""
                                for a in ajouts:
                                    html_add += f"""
                                                            <div style="
                                                                display: inline-block;
                                                                background-color: #fdebd0; 
                                                                border-left: 4px solid #f39c12; 
                                                                padding: 6px 12px; 
                                                                border-radius: 4px; 
                                                                margin: 0px 8px 8px 0px; 
                                                                color: #7e5109; 
                                                                font-weight: 500;
                                                                font-size: 14px;
                                                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                                            ">
                                                                {a}
                                                            </div>
                                                            """
                                st.markdown(html_add, unsafe_allow_html=True)
                            else:
                                st.write("Aucune invention")
            else:
                st.info("Aucun détail d'erreur répertorié")
    else:
        st.info(
            "Fichier introuvable. Veuillez vérifier que votre fichier est dans le bon dossier")

    afficher_footer()