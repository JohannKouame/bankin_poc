import streamlit as st
import logging
import click

from src.pages.dashboard import display_dashboard
from src.pages.chat import display_chat
from src.logger.logger import Logger

@click.command()
def run_streamlit():
    Logger()
    st.set_page_config(page_title="POC Bankin Simulation", layout="wide")
    st.title("POC Bankin Simulation by Johann KOUAMÉ")

    st.markdown(
        """
        <div style="
            background-color: #F5F7FA;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            margin-bottom: 15px;
        ">
            <h4 style="margin-top:0;">Bienvenue dans votre assistant d’analyse de dépenses</h4>
            <p style="margin-bottom:0;">
                Cette application simule un assistant d’analyse de dépenses basé
                sur des transactions fictives.
                Consultez le récapitulatif, choisissez une période, puis posez vos
                questions dans le chat.
                Exemples :
            </p>
            <ul>
                <li>Où est-ce que je dépense le plus ?</li>
                <li>Mes dépenses augmentent-elles ?</li>
                <li>Comment optimiser mon budget ?</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    logging.info("Chat and dashboard init")
    display_dashboard()
    display_chat()


if __name__ == "__main__":
    run_streamlit()
