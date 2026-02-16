import pandas as pd
import logging

from src.command.download_dataset import LOGGING_VARIABLE
from src.logger.logger import Logger

# Initialisation unique du logger
Logger()


class TransactionProcessor:
    def __init__(self, df: pd.DataFrame):
        logging.info("Initialisation du TransactionProcessor")
        self.df = df.copy()
        self.monthly_summary = None
        self.sub_categories_stats = None
        self.flexible_stats = None
        logging.debug(f"DataFrame initial:\n{self.df.head()}")

    def format_date_and_amount(self):
        logging.info("Début format_date_and_amount")
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['amount'] = self.df['amount'].astype(float)
        logging.debug(f"DataFrame après format_date_and_amount:\n{self.df.head()}")
        logging.info("Fin format_date_and_amount")
        return self

    def get_n_first_month_transactions(self, n: int):
        logging.info(f"Début get_n_first_month_transactions avec n={n}")
        self.df = self.df.sort_values(by='date', ascending=True)
        start_date = self.df['date'].min()
        end_date = start_date + pd.DateOffset(months=n)
        self.df = self.df[self.df['date'] <= end_date]
        logging.debug(f"DataFrame après filtrage {n} premiers mois:\n{self.df.head()}")
        logging.info("Fin get_n_first_month_transactions")
        return self

    def map_and_split_categories(self, mapping: dict):
        logging.info("Début map_and_split_categories")
        self.df['mapped_category'] = self.df['category'].map(mapping)
        self.df['main_category'] = self.df['mapped_category'].apply(
            lambda x: x.split('/')[0] if isinstance(x, str) and '/' in x else x
        )
        self.df['sub_category'] = self.df['mapped_category'].apply(
            lambda x: x.split('/')[1] if isinstance(x, str) and '/' in x else x
        )
        logging.debug(f"DataFrame après map_and_split_categories:\n{self.df.head()}")
        logging.info("Fin map_and_split_categories")
        return self

    def create_year_month_feature(self):
        logging.info("Début create_year_month_feature")
        self.df['year_month'] = self.df['date'].dt.to_period('M')
        logging.debug(f"DataFrame après création year_month:\n{self.df.head()}")
        logging.info("Fin create_year_month_feature")
        return self

    def aggregate_per_year_month(self):
        logging.info("Début aggregate_per_year_month")
        self.monthly_summary = self.df.groupby(
            ['year_month', 'main_category', 'sub_category']
        )['amount'].sum().reset_index()
        logging.debug(f"monthly_summary:\n{self.monthly_summary.head()}")
        logging.info("Fin aggregate_per_year_month")
        return self

    def get_operation_count_per_category(self):
        logging.info("Début get_operation_count_per_category")
        # Vérifie que monthly_summary existe
        if self.monthly_summary is None:
            logging.info("monthly_summary inexistant, on l'agrège d'abord")
            self.aggregate_per_year_month()

        # Ajout de operation_count si inexistant
        if 'operation_count' not in self.monthly_summary.columns:
            avg_monthly_operation_per_category = self.monthly_summary.groupby(
                ["year_month", "main_category", "sub_category"]
            )['amount'].count().reset_index()
            avg_monthly_operation_per_category.rename(columns={'amount': 'operation_count'}, inplace=True)
            self.monthly_summary = self.monthly_summary.merge(
                avg_monthly_operation_per_category,
                on=["year_month", "main_category", "sub_category"],
                how='left'
            )
        logging.debug(f"monthly_summary après ajout operation_count:\n{self.monthly_summary.head()}")
        logging.info("Fin get_operation_count_per_category")
        return self

    def get_sub_categories_stats(self):
        logging.info("Début get_sub_categories_stats")
        amount_stats = self.monthly_summary.groupby(['sub_category', 'main_category'])['amount'].agg(['std', 'max', 'min', 'mean', 'median']).reset_index()
        amount_stats.rename(columns={
            'std': 'amount_std', 'max': 'amount_max', 'min': 'amount_min',
            'mean': 'amount_mean', 'median': 'amount_median'
        }, inplace=True)
        amount_stats.fillna(0, inplace=True)
        for col in amount_stats.select_dtypes('float64').columns:
            amount_stats[col] = amount_stats[col].round(2)

        operation_stats = self.monthly_summary.groupby(['sub_category', 'main_category'])['operation_count'].agg(['std', 'max', 'min', 'mean', 'median']).reset_index()
        operation_stats.rename(columns={
            'std': 'operation_count_std', 'max': 'operation_count_max',
            'min': 'operation_count_min', 'mean': 'operation_count_mean', 'median': 'operation_count_median'
        }, inplace=True)
        operation_stats.fillna(0, inplace=True)
        for col in operation_stats.select_dtypes('float64').columns:
            operation_stats[col] = operation_stats[col].round(2)

        self.sub_categories_stats = amount_stats.merge(
            operation_stats,
            on=['sub_category', 'main_category'],
            how='left'
        )
        logging.debug(f"sub_categories_stats:\n{self.sub_categories_stats.head()}")
        logging.info("Fin get_sub_categories_stats")
        return self

    def get_flexible_categories_stats(self, flexible_categories: list):
        logging.info(f"Début get_flexible_categories_stats pour {flexible_categories}")
        self.flexible_stats = self.df[self.df['main_category'].isin(flexible_categories)]
        logging.debug(f"flexible_stats:\n{self.flexible_stats.head()}")
        logging.info("Fin get_flexible_categories_stats")
        return self

    def get_proportion_to_cut(self, amount: float):
        logging.info(f"Début get_proportion_to_cut pour amount={amount}")
        if 'year_month' not in self.df.columns:
            logging.info("year_month inexistant, création automatique")
            self.create_year_month_feature()
        monthly_total_mean = self.df.groupby('year_month')['amount'].sum().mean()
        saving_ratio = amount / monthly_total_mean
        logging.debug(f"saving_ratio calculé: {saving_ratio}")
        logging.info("Fin get_proportion_to_cut")
        return saving_ratio
