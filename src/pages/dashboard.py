import streamlit as st
import pandas as pd
from src.utils.loader import Loader

def display_dashboard():
    """
    Display streamlit dashboard
    """
    monthly_summary = Loader.csv_loader("data/processed/monthly_summary.csv")
    monthly_summary["year_month"] = pd.to_datetime(monthly_summary["year_month"])
    monthly_summary_sorted = monthly_summary.sort_values("year_month")
    unique_months = monthly_summary_sorted["year_month"].unique()
    n_months = len(unique_months)

    # Filter options
    filter_options = ["1 mois", "3 mois", "6 mois", "9 mois"]
    selection = st.segmented_control(
        "Période",
        filter_options,
        selection_mode="single",
        default="1 mois"
    )
    n_selected_months = min(int(selection.split()[0]), n_months)

    start_period = monthly_summary_sorted["year_month"].min()
    end_period = start_period + pd.DateOffset(months=n_selected_months - 1)

    filtered_df = monthly_summary_sorted[
        (monthly_summary_sorted["year_month"] >= start_period) &
        (monthly_summary_sorted["year_month"] <= end_period)
        ]

    st.markdown(f"### Bilan sur {selection}")
    start_label = start_period.strftime("%B %Y")
    end_label = end_period.strftime("%B %Y")
    st.caption(f"Période couverte : {start_label} → {end_label}")

    total_spent = filtered_df["amount"].sum()
    avg_per_month = filtered_df.groupby("year_month")["amount"].sum().mean()

    # Display general information
    col1, col2 = st.columns(2)
    col1.metric("Dépenses Totales", f"{round(total_spent, 2)} €")
    col2.metric("Dépense moyenne / mois", f"{round(avg_per_month, 2)} €")

    # Display filtered table
    filtered_df["Période"] = filtered_df["year_month"].dt.strftime("%B %Y")
    filtered_df = filtered_df.reset_index(drop=True)

    st.subheader("Aperçu des transactions")
    st.caption(f"Transactions de {start_label} à {end_label}")
    st.dataframe(filtered_df[["Période", "main_category", "sub_category", "amount"]].head(5))
