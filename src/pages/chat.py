import streamlit as st
import logging
from src.client.mistral import MistralClient
from src.repository.mistral_repository import MistralRepository
from src.utils.loader import Loader
from src.logger.logger import Logger

LOGGING_VARIABLE = "[CHAT]"

Logger()

# Init model
mistral = MistralRepository(MistralClient())

def display_chat():
    """
    Display chat and manage history
    """
    # Set chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Set and manage user input
    if prompt := st.chat_input("Écrivez votre message ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        logging.debug(f"{LOGGING_VARIABLE} Utilisateur a envoyé : {prompt}")

        # Model response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            try:
                # Streaming Mistral
                stream = mistral.preprocess_and_answer(
                    message=prompt,
                    stats=Loader.csv_loader_and_formater("data/processed/monthly_summary.csv")
                )

                for token in stream:
                    full_response += token
                    placeholder.markdown(full_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                logging.debug(f"{LOGGING_VARIABLE} Réponse complète du modèle : {full_response}")

            except Exception as e:
                logging.error(f"{LOGGING_VARIABLE} Erreur lors de l'appel au modèle : {e}")
                placeholder.markdown("Erreur lors de l'appel au modèle, réessayez plus tard.")
