import streamlit as st

import streamlit as st


def afficher_footer():
    # Injection du code CSS pour fixer le footer en bas et ajuster la marge
    st.markdown(
        """
        <style>
        /* Force le conteneur principal à avoir une marge en bas pour 
           que le texte ne se cache pas derrière le footer à la fin du défilement */
        .block-container {
            padding-bottom: 80px;
        }

        /* Style du footer fixe */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2c323d; /* Couleur de fond (gris très clair) */
            color: #888888;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            z-index: 100; /* S'assure que le footer reste toujours au-dessus du reste */
        }
        </style>

        <div class="footer">
            Fait avec ❤️ par <b>Florias Tokotchi</b> et <b>Amos</b> | Copyright © 2026 - Projet TER - Master 1 ATAL - Nantes Université
        </div>
        """,
        unsafe_allow_html=True
    )