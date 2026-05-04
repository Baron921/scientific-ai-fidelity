import streamlit as st
import streamlit_antd_components as sac


def afficher_menu():
    with st.sidebar:
        st.markdown("### 🧭 Menu Principal")

        selected = sac.menu([
            sac.MenuItem('Accueil', icon='house'),
            sac.MenuItem('Données', icon='database-fill-up'),

            sac.MenuItem('Évaluation factuelle', icon='play-circle', children=[
                sac.MenuItem('Metrics', icon='bar-chart'),
                sac.MenuItem('NER', icon='tag'),
            ]),

            #sac.MenuItem('Évaluation factuelle', icon='shield-check'),

            # Tu peux aussi faire pareil pour "Évaluation factuelle" si besoin plus tard :
            # sac.MenuItem('Évaluation factuelle', icon='shield-check', children=[
            #     sac.MenuItem('Sous-partie 1'),
            #     sac.MenuItem('Sous-partie 2')
            # ]),

            sac.MenuItem('Configuration', icon='sliders'),
            sac.MenuItem('À propos', icon='info-circle'),
        ],
            format_func='title',
            open_all=False,
            size='md',
            color='#007BFF',
            variant='filled'
        )

    return selected