import streamlit as st
import logging
import pandas as pd

from src.client.mistral import MistralClient
from src.repository.mistral_repository import MistralRepository
from src.utils.loader import Loader
# --- Logger pour le terminal ---
logger = logging.getLogger("bankin_llm")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.info("Démarrage de l'application Streamlit")

st.title("POC Bankin Simulation")
st.write("Bienvenue dans votre assistant d'analyse de dépenses !")

# --- Initialisation du client Mistral ---
logger.info("Initialisation du client Mistral")
mistral = MistralRepository(MistralClient())





monthly_summary = Loader.csv_loader("data/processed/monthly_summary.csv")

n_months = len(monthly_summary["year_month"].unique())
# --- Résumé rapide ---
total_spent = monthly_summary['amount'].sum()
avg_per_month = monthly_summary['amount'].mean()
top_categories = monthly_summary.groupby('main_category')['amount'].sum().sort_values(ascending=False).head(3)

# --- Encadré profil utilisateur fictif ---
with st.expander("Profil et contexte de la personne"):
    col1, col2= st.columns(2)
    col1.metric("Dépenses Total", f"{round(total_spent, 2)} €")
    col2.metric("Dépense moyenne", f"{round(avg_per_month, 2)} €")
    #col3.metric("Humidity", "86%", "4%")
    st.write("Top 3 catégories :", ", ".join(top_categories.index))

    st.subheader("Aperçu des transactions")
    st.dataframe(monthly_summary.head(5))  # Affiche les 5 premières lignes

# --- Historique de la conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Affichage des messages précédents ---
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        st.markdown(content)

# --- Input utilisateur ---
if prompt := st.chat_input("Écrivez votre message ici..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    logger.debug(f"Utilisateur a envoyé : {prompt}")

    # Appel au modèle Mistral pour générer la réponse
    with st.chat_message("assistant"):
        try:
            response = mistral.chat(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            logger.debug(f"Réponse du modèle : {response}")
        except Exception as e:
            logger.error(f"Erreur lors de l'appel au modèle : {e}")
            st.error(f"Erreur lors de l'appel au modèle : {e}")
