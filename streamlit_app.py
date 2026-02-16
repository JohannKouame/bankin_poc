import streamlit as st

from src.logger.logger import Logger
from src.pages.dashboard import Dashboard
from src.pages.chat import ChatInterface


def run_streamlit():
    Logger()
    st.title("POC Bankin Simulation by Johann KOUAMÉ")

    # Affichage intro
    Dashboard.show_intro()

    # Initialiser la donnée et le dashboard
    df = Dashboard.load_data("data/processed/monthly_summary.csv")
    Dashboard.show_metrics(df)

    # Chat
    ChatInterface.display_chat()


if __name__ == "__main__":
    run_streamlit()
