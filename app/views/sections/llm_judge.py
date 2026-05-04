import streamlit as st
import plotly.express as px


def afficher_llm_judge(data):
    # st.divider()
    st.header("Évaluation par LLM & Corrélations")
    # st.markdown("Analyse des corrélations entre les scores des experts IA (LLM) et les métriques automatiques.")

    tab_j1, tab_j2 = st.tabs(["Sémantique & LLM", "Factuel & LLM"])

    # --- TAB 1 : CORRÉLATIONS SÉMANTIQUE ---
    with tab_j1:
        st.markdown("##### Correlations between AI expert annotator scores and semantic metrics")

        sem_cols = [col for col in data.columns if col.startswith(("Be", "Ba", "sem"))]

        if sem_cols:
            sem_df_numeric = data[sem_cols].select_dtypes(include='number')
            sem_cors = sem_df_numeric.corr()

            lignes_llm = [c for c in sem_cors.index if c.startswith("sem")]

            if lignes_llm:
                sem_cors_sliced = sem_cors.loc[lignes_llm, :]

                # Le .values (sans z=) empêche l'erreur 'dtype' de Plotly
                fig_sem = px.imshow(
                    sem_cors_sliced.values,
                    x=sem_cors_sliced.columns,
                    y=sem_cors_sliced.index,
                    text_auto=".2f",
                    color_continuous_scale="Blues",
                    aspect="auto"
                )

                fig_sem.update_layout(xaxis_title="", yaxis_title="", xaxis_tickangle=-45,
                                      margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_sem, use_container_width=True)
            else:
                st.warning("⚠️ Aucune ligne correspondant au juge sémantique ('sem') trouvée.")
        else:
            st.warning("⚠️ Les colonnes sémantiques (Be, Ba, Co, sem) sont introuvables.")

    # --- TAB 2 : CORRÉLATIONS FACTUEL ---
    with tab_j2:
        st.markdown("##### Correlations between AI expert annotator scores and factual metrics")

        fact_cols = [col for col in data.columns if col.startswith(("Fa", "fa"))]

        if fact_cols:
            fact_df_numeric = data[fact_cols].select_dtypes(include='number')
            fact_cors = fact_df_numeric.corr()

            lignes_llm_fact = [c for c in fact_cors.index if c.startswith("fa")]

            if lignes_llm_fact:
                fact_cors_sliced = fact_cors.loc[lignes_llm_fact, :]

                # Même logique robuste pour le factuel
                fig_fact = px.imshow(
                    fact_cors_sliced.values,
                    x=fact_cors_sliced.columns,
                    y=fact_cors_sliced.index,
                    text_auto=".2f",
                    color_continuous_scale="Blues",
                    aspect="auto"
                )

                fig_fact.update_layout(xaxis_title="", yaxis_title="", xaxis_tickangle=-45,
                                       margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_fact, use_container_width=True)
            else:
                st.warning("⚠️ Les colonnes du juge factuel ('fa') sont introuvables.")
        else:
            st.warning("⚠️ Les colonnes factuelles sont introuvables.")