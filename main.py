# main.py
from dotenv import load_dotenv
import os
import sys
import logging
from typing import Optional
import warnings
import pandas as pd
from pathlib import Path



if os.getenv('etl_log_level') is None:
     etl_log_level = 20
else:
     etl_log_level = int(os.getenv('etl_log_level'))

warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

def _setup_logger(etl_log_level: int=20) -> logging.Logger:
        """
        Set up a logger for the Drug_Review_Sentiment ETL.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger("DRUG_REVIEW_SENTIMENT")
        # logger.setLevel(logging.INFO)
        logger.setLevel(etl_log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not logger.hasHandlers():
            logger.addHandler(handler)
        return logger

def setup_project_env():
    global project_dir
    """Loads environment variables and sets up the project's Python path."""
    app_logger.info("Attempting to run env setup")
    # Load .env file from the project root
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    load_dotenv(dotenv_path=os.path.join(project_dir, '.env'))
    # Read PYTHONPATH from .env and add to sys.path
    pythonpath = os.getenv('PYTHONPATH')
    if pythonpath:
        # Split multiple paths if necessary (e.g., if you set PYTHONPATH=path1:path2)
        paths = pythonpath.split(os.pathsep)
        for path in paths:
            abs_path = os.path.abspath(os.path.join(project_dir, path))
            if abs_path not in sys.path:
                sys.path.insert(0, abs_path)
                app_logger.info(f"Added '{abs_path}' to Python path.")

def run_processing():
    # Importing your actual pipeline functions
    from helper_function.data_load import Data_load
    from helper_function.ml_flow_tracking import run_mlflow_tracking

    reader = Data_load()
    drug_train_raw = reader.read_tsv("drugLibTest_raw.tsv")
    drug_train_raw.rename(columns={"Unnamed: 0":"id"}, inplace=True)
    cols_to_concat = ['benefitsReview', 'sideEffectsReview', 'commentsReview']

    # drug_processed_df = generate_text_transformation(drug_train_raw,cols_to_concat)

    # display(drug_train_processed[['clean_text','combined_text']])

    # display(drug_processed_df)
    run_mlflow_tracking(drug_train_raw, cols_to_concat=cols_to_concat)


print(type(etl_log_level))
app_logger = _setup_logger(etl_log_level)

app_logger.info(f"Log level is set to {logging.getLevelName(etl_log_level)}")
app_logger.info(f"main.py >> executing as {__name__}")

if __name__ != "__main__":
     setup_project_env()

else:
     setup_project_env()
     app_logger.info(f"Default path is set to >> {project_dir}")
     app_logger.info(f"starting ETL process....")
     run_processing()


     




