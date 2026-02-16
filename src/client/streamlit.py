# repository/streamlit_repository.py
import pandas as pd
from src.utils.preprocessing import TransactionProcessor

class StreamlitClient:
    def load_data(self, file) -> pd.DataFrame:
        df = pd.read_csv(file)
        return df

    def process_transactions(self, df: pd.DataFrame, n_months: int) -> pd.DataFrame:
        # Exemple simple de pipeline
        processor = TransactionProcessor(df)
        processor.format_date_and_amount() \
            .get_n_first_month_transactions(n_months) \
            .map_and_split_categories(mapping={}) \
            .create_year_month_feature() \
            .aggregate_per_year_month() \
            .get_operation_count_per_category() \
            .get_sub_categories_stats()
        return processor.sub_categories_stats

    def calculate_saving_ratio(self, df: pd.DataFrame, target_amount: float) -> float:
        processor = TransactionProcessor(df)
        processor.create_year_month_feature()
        return processor.get_proportion_to_cut(target_amount)
