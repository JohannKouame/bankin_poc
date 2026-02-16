# client/run_streamlit.py
import streamlit as st
#from src.client.streamlit import StreamlitClient

class StreamlitRepository:
    def __init__(self):
        self.repo = StreamlitClient()

    def run(self):
        st.title("POC Bankin SImulation")

        st.write("Bienvenue dans votre assistant d'analyse de dépenses !")

        user_message = st.text_input(label="Que souhaitez vous ?")
        # Upload du CSV
        uploaded_file = st.file_uploader("Choisissez votre fichier CSV", type="csv")
        if uploaded_file:
            df = self.repo.load_data(uploaded_file)
            st.subheader("Aperçu des transactions")
            st.dataframe(df.head())

            # Choix du nombre de mois
            n_months = st.slider("Nombre de mois à analyser", min_value=1, max_value=12, value=6)

            # Traitement
            processed_df = self.repo.process_transactions(df, n_months)
            st.subheader(f"Résumé sur {n_months} mois")
            st.dataframe(processed_df.head())

            # Calcul proportion à épargner
            target_saving = st.number_input("Objectif d'épargne (€)", min_value=0, value=500)
            saving_ratio = self.repo.calculate_saving_ratio(processed_df, target_saving)
            st.info(f"Pour atteindre {target_saving} €, vous devez réduire environ {saving_ratio*100:.2f}% de vos dépenses moyennes mensuelles.")
