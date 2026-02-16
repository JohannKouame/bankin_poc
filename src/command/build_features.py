import pandas as pd
import click
import os
import traceback
import logging


from src.utils.preprocessing import TransactionProcessor
from src.utils.loader import Loader
from src.logger.logger import Logger

Logger()
@click.command()
def build_features():
    try:
        # Charger le CSV
        df = Loader.csv_loader("data/raw/budget_data.csv")

        # Mapping catégories
        category_mapping = Loader.json_loader("categories_mapping.json")

        # Pipeline preprocessing
        processor = (TransactionProcessor(df)
                     .format_date_and_amount()
                     .get_n_first_month_transactions(9)
                     .map_and_split_categories(category_mapping)
                     .create_year_month_feature()
                     .aggregate_per_year_month()
                     .get_operation_count_per_category()
                     .get_sub_categories_stats()
                     )

        # Accéder au résultat
        processor.monthly_summary.to_csv("data/processed/monthly_summary.csv")
        processor.sub_categories_stats.to_csv("data/processed/sub_categories_stats.csv")
    except Exception as error:
        if os.getenv("DEBUG_MODE") == "1":
            print(traceback.format_exc())
        logging.exception(f"An error occurred when running `build_features` command")

if __name__ == "__main__":
    build_features()
