import streamlit as st
import pandas as pd

class Dashboard:

    @staticmethod
    def show_intro():
        st.markdown("""
        <div style="
            background-color: #F5F7FA;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            margin-bottom: 15px;
        ">
        <h4 style="margin-top:0;">Bienvenue dans votre assistant d’analyse de dépenses</h4>
        <p>Cette application simule un assistant d’analyse de dépenses basé sur des transactions fictives. Consultez le récapitulatif, choisissez une période, puis posez vos questions dans le chat.</p>
        <ul>
        <li>Où est-ce que je dépense le plus ?</li>
        <li>Mes dépenses augmentent-elles ?</li>
        <li>Comment optimiser mon budget ?</li>
        </ul>
        <a href="https://github.com/JohannKouame/bankin_poc" target="_blank">Lien du repo Github</a>
        <p style="margin-top:10px; font-size:0.9em; color:#555;">NB : Il s'agit d'un POC. Le modèle ne possède pas de mémoire et ne peut donc pas réagir sur ses anciennes réponses.</p>
        </div>
        """, unsafe_allow_html=True)


    @staticmethod
    def load_data(path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        df["year_month"] = pd.to_datetime(df["year_month"])
        return df.sort_values("year_month")

    @staticmethod
    def show_metrics(df: pd.DataFrame):
        filter_options = ["1 mois", "3 mois", "6 mois", "9 mois"]
        selection = st.segmented_control(
            "Période",
            filter_options,
            selection_mode="single",
            default="1 mois"
        )

        n_selected_months = int(selection.split()[0])
        unique_months = df["year_month"].nunique()
        n_selected_months = min(n_selected_months, unique_months)

        start_period = df["year_month"].min()
        end_period = start_period + pd.DateOffset(months=n_selected_months - 1)

        filtered_df = df[(df["year_month"] >= start_period) & (df["year_month"] <= end_period)]

        st.markdown(f"### Bilan sur {selection}")
        st.caption(f"Période couverte : {start_period.strftime('%B %Y')} → {end_period.strftime('%B %Y')}")

        total_spent = filtered_df["amount"].sum()
        avg_per_month = filtered_df.groupby("year_month")["amount"].sum().mean()

        col1, col2 = st.columns(2)
        col1.metric("Dépenses Totales", f"{round(total_spent, 2)} €")
        col2.metric("Dépense moyenne / mois", f"{round(avg_per_month, 2)} €")

        # Affichage aperçu
        filtered_df = filtered_df.copy()
        filtered_df["Période"] = filtered_df["year_month"].dt.strftime("%B %Y")
        st.subheader("Aperçu des transactions")
        st.caption(f"Transactions de {start_period.strftime('%B %Y')} à {end_period.strftime('%B %Y')}")
        st.dataframe(filtered_df[["Période", "main_category", "sub_category", "amount"]].head(5))
        st.markdown("---")
