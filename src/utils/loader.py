import json
import pandas as pd
import os
import kagglehub
from kagglehub import KaggleDatasetAdapter

class Loader:
    @staticmethod
    def downloader(url: str, saving_directory: str, file_name: str = "budget_data.csv") -> pd.DataFrame:
        """
        Télécharge un dataset Kaggle et sauvegarde un CSV localement.

        Args:
            url (str): Le slug du dataset Kaggle (ex: "ismetsemedov/personal-budget-transactions-dataset")
            saving_directory (str): Dossier où stocker le CSV
            file_name (str): Nom du fichier CSV à créer

        Returns:
            pd.DataFrame: Contenu du dataset sous forme de DataFrame
        """

        df = kagglehub.dataset_load(
            KaggleDatasetAdapter.PANDAS,
            url,
            file_name,
        )

        df.to_csv(saving_directory, index=False)
        return df


    @staticmethod
    def json_loader(path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            file = json.load(f)
        return file


    @staticmethod
    def csv_loader(path: str, ignore_first_col: bool = False) -> pd.DataFrame:
        if ignore_first_col:
            return pd.read_csv(path, index_col=0)
        else:
            return pd.read_csv(path)


    @staticmethod
    def csv_loader_and_formater(path: str) -> str:
        df = Loader.csv_loader(path)
        df = df.drop(columns=[col for col in df.columns if "Unnamed" in col], errors="ignore")

        # Aggregate
        grouped = (
            df.groupby(["year_month", "main_category", "sub_category"], as_index=False)
            .agg({
                "amount": "sum",
                "operation_count": "sum"
            })
        )

        # Transformation en dictionnaire imbriqué
        result = {}

        for _, row in grouped.iterrows():
            ym = row["year_month"]
            mc = row["main_category"]
            sc = row["sub_category"]

            result.setdefault(ym, {})
            result[ym].setdefault(mc, {})
            result[ym][mc][sc] = {
                "amount": row["amount"],
                "operation_count": int(row["operation_count"])
            }

        return json.dumps(result, indent=4, ensure_ascii=False)
