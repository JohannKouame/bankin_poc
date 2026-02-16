import streamlit as st
import click
import logging

from src.client.mistral import MistralClient
from src.repository.mistral_repository import MistralRepository
from src.utils.loader import Loader
from src.logger.logger import Logger

@click.command()
def run_streamlit():
    Logger()

    st.title("POC Bankin Simulation")
    st.write("Bienvenue dans votre assistant d'analyse de dépenses !")

    # Init Mistral model
    logging.info("Initialisation du client Mistral")
    mistral = MistralRepository(MistralClient())

    # Load monthly_summary
    monthly_summary = Loader.csv_loader("data/processed/monthly_summary.csv")

    # Get some information about user transaction
    n_months = len(monthly_summary["year_month"].unique())
    total_spent = monthly_summary['amount'].sum()
    avg_per_month = monthly_summary['amount'].mean()

    # Display user transaction summary
    with st.expander("Profil et contexte de la personne"):
        col1, col2= st.columns(2)
        col1.metric("Dépenses Total", f"{round(total_spent, 2)} €")
        col2.metric("Dépense moyenne", f"{round(avg_per_month, 2)} €")

        st.subheader("Aperçu des transactions")
        st.dataframe(monthly_summary.head(5))

    # Set conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display conversation history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)

    # Set user input box
    if prompt := st.chat_input("Écrivez votre message ici..."):
        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        logging.debug(f"Utilisateur a envoyé : {prompt}")

        # Call mistral model
        with st.chat_message("assistant"):
            try:
                response = mistral.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                logging.debug(f"Réponse du modèle : {response}")
            except Exception as e:
                logging.error(f"Erreur lors de l'appel au modèle : {e}")
                st.error(f"Erreur lors de l'appel au modèle : {e}")

if __name__ == '__main__':
    run_streamlit()