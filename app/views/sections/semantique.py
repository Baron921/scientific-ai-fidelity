import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

def afficher_semantique(data):
    st.header("Qualité Sémantique & Cohérence")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Quartiles",
        "Corrélations",
        "BertScore",
        "BartScore"
    ])

    filtres = st.session_state.get('filtre_semantique', ["BertScore", "BartScore", "Cos_Sim"])

    # --- TAB 1 : TABLEAU DES QUARTILES ---
    with tab1:
        st.markdown("##### Table 1 : Quartiles of semantic and textual coherence metrics across prompts")
        metriques_cibles = [
            "BertScore1", "BertScore2", "BertScore3",
            "BartScore1", "BartScore2", "BartScore3",
            "Cos_Sim1", "Cos_Sim2", "Cos_Sim3"
        ]
        metriques_presentes = [m for m in metriques_cibles if m in data.columns]

        if metriques_presentes:
            gen_stats = data[metriques_presentes].describe()
            table_quartiles = gen_stats.T[['25%', '50%', '75%', 'mean']].rename(
                columns={'25%': 'Q1', '50%': 'Q2 (Median)', '75%': 'Q3', 'mean': 'Mean'})

            styled_table = table_quartiles.style.format("{:.2f}")
            #for prefix in ['Bert', 'Bart', 'Cos']:
                #groupe_lignes = [idx for idx in table_quartiles.index if prefix in idx]
                #if groupe_lignes:
                    #styled_table = styled_table.background_gradient(subset=(groupe_lignes, table_quartiles.columns), axis=0)

            def highlight_max_per_group(df_to_style):
                styles = pd.DataFrame('', index=df_to_style.index, columns=df_to_style.columns)
                for prefix in ['Bert', 'Bart', 'Cos']:
                    groupe_lignes = [idx for idx in df_to_style.index if prefix in idx]
                    if groupe_lignes:
                        for col in df_to_style.columns:
                            val_max = df_to_style.loc[groupe_lignes, col].max()
                            for idx in groupe_lignes:
                                if df_to_style.loc[idx, col] == val_max:
                                    styles.loc[idx, col] = 'font-weight: bold;'
                return styles

            styled_table = styled_table.apply(highlight_max_per_group, axis=None)
            st.dataframe(styled_table, use_container_width=True)
        else:
            st.warning("⚠️ Les colonnes exactes sont introuvables.")

    # --- TAB 2 : HEATMAP DES CORRÉLATIONS ---
    with tab2:
        st.markdown("##### Figure 2: Semantic and textual coherence metrics correlations")
        cols_corr = [
            "BertScore1", "BartScore1", "Cos_Sim1",
            "BertScore2", "BartScore2", "Cos_Sim2",
            "BertScore3", "BartScore3", "Cos_Sim3"
        ]
        cols_presentes = [c for c in cols_corr if c in data.columns]

        if len(cols_presentes) > 1:
            corr_matrix = data[cols_presentes].corr()
            fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="Blues", aspect="square")
            fig_corr.update_layout(xaxis_title="", yaxis_title="", xaxis_tickangle=-90,
                                   margin=dict(l=20, r=20, t=20, b=20))
            fig_corr.update_xaxes(side="bottom")
            st.plotly_chart(fig_corr, use_container_width=True)


    def tracer_boxplot_semantique(metrique, *vline):
        if 'Domaine' in data.columns:
            cols = [f"{metrique}1", f"{metrique}2", f"{metrique}3"]

            # On vérifie si les colonnes existent
            if all(c in data.columns for c in cols):

                # Melt des données
                df_long = data[["Domaine"] + cols].melt(
                    id_vars=["Domaine"],
                    value_vars=cols,
                    var_name="Version",
                    value_name=metrique
                )

                # Création de la figure Matplotlib / Seaborn
                fig, ax = plt.subplots(figsize=(10, 6))

                sns.boxplot(
                    data=df_long,
                    y="Domaine",
                    x=metrique,
                    hue="Version",
                    ax=ax,
                    palette=["#1f77b4", "#ff7f0e", "#2ca02c"]  # Pour garder la charte graphique Streamlit
                )

                # L'ajout des lignes verticales (*vline) exactement comme dans le Jupyter !
                if vline:
                    for val in vline:
                        ax.axvline(x=val, linestyle="--", linewidth=1.5)
                        # Le label textuel (0.85, 0.9, -1.5) positionné au milieu
                        ax.text(val, ax.get_ylim()[1] / 2, f"{val}", rotation=0, va='bottom', fontsize=10)

                # Le titre exact
                ax.set_title(f"Comparison of {metrique} across rewrites")
                plt.tight_layout()

                # Affichage dans Streamlit
                st.pyplot(fig)
            else:
                st.warning(f"⚠️ Colonnes {metrique} introuvables.")

    # --- TAB 3 : BertScore ---
    with tab3:
        if "BertScore" in filtres:
            st.markdown("##### BertScore boxplots across prompts")
            # Appel exact avec les deux seuils : 0.85 et 0.9
            tracer_boxplot_semantique("BertScore", 0.85, 0.9)
        else:
            st.info("L'affichage du BertScore est désactivé dans la configuration.")

    # --- TAB 4 : BartScore ---
    with tab4:
        st.markdown("##### BartScore boxplots across prompts")
        # Appel exact avec le seuil : -1.5
        tracer_boxplot_semantique("BartScore", -1.5)
