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

        df = kagglehub.load_dataset(
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
    def csv_loader(path: str) -> pd.DataFrame:
        return pd.read_csv(path, index_col=0)
