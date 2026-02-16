import click
import os
import traceback
import logging

from src.logger.logger import Logger
from src.utils.loader import Loader

Logger()

LOGGING_VARIABLE="[DATASET_DOWNLOADER"

@click.command()
@click.option("--url", default="ismetsemedov/personal-budget-transactions-dataset", help="Download Kaggle dataset")
def download_dataset(url):
    """Consume an AMQP queue to regenerate products or users."""
    try:
        saving_directory = "./data/raw/budget_data.csv"
        Loader.downloader(url=url, saving_directory=saving_directory)
        logging.info(f"Dataset downloaded and saved with success : {saving_directory}")
    except Exception as error:
        if os.getenv("DEBUG_MODE") == "1":
            print(traceback.format_exc())
        logging.exception(f"An error occurred when running `download_dataset` command")


if __name__ == "__main__":
    download_dataset()
