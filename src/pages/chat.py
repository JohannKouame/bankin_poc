import streamlit as st
import logging
import time
from src.repository.mistral_repository import MistralRepository
from src.client.mistral import MistralClient


class ChatInterface:

    @staticmethod
    def display_chat():
        mistral = MistralRepository(MistralClient())

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Afficher l'historique
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Entrée utilisateur
        if prompt := st.chat_input("Écrivez votre message ici..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)
            logging.debug(f"Utilisateur a envoyé : {prompt}")

            # Obtenir la réponse depuis MistralRepository
            try:
                response = mistral.chat(prompt)
            except Exception as e:
                logging.error(f"Erreur lors de l'appel au modèle : {e}")
                response = "Erreur lors de l'appel au modèle, réessaie plus tard."

            # Affichage progressif
            with st.chat_message("assistant"):
                placeholder = st.empty()
                displayed_text = ""
                if len(response.split()) < 50:
                    placeholder.markdown(response)
                else:
                    with st.spinner("Mistral écrit sa réponse..."):
                        for chunk in response.split(". "):
                            displayed_text += chunk + ". "
                            placeholder.markdown(displayed_text)
                            time.sleep(0.05)

            st.session_state.messages.append({"role": "assistant", "content": response})
            logging.debug(f"Réponse du modèle : {response}")
