# main.py
from dotenv import load_dotenv
import os
import sys
import logging
from typing import Optional

if os.getenv('log_level') is None:
     log_level = 20
else:
     log_level = int(os.getenv('log_level'))

def _setup_logger(log_level: int=20) -> logging.Logger:
        """
        Set up a logger for the Drug_Review_Sentiment ETL.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger("DRUG_REVIEW_SENTIMENT")
        # logger.setLevel(logging.INFO)
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not logger.hasHandlers():
            logger.addHandler(handler)
        return logger

def setup_project_env():
    """Loads environment variables and sets up the project's Python path."""
    app_logger.info("Attempting to run env setup")
    # Load .env file from the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    load_dotenv(dotenv_path=os.path.join(project_root, '.env'))
    # Read PYTHONPATH from .env and add to sys.path
    pythonpath = os.getenv('PYTHONPATH')
    if pythonpath:
        # Split multiple paths if necessary (e.g., if you set PYTHONPATH=path1:path2)
        paths = pythonpath.split(os.pathsep)
        for path in paths:
            abs_path = os.path.abspath(os.path.join(project_root, path))
            if abs_path not in sys.path:
                sys.path.insert(0, abs_path)
                app_logger.info(f"Added '{abs_path}' to Python path.")


print(type(log_level))
app_logger = _setup_logger(log_level)

app_logger.info(f"Log level is set to {logging.getLevelName(log_level)}")
app_logger.info(f"main.py >> executing as {__name__}")
if __name__ != "__main__":
     setup_project_env()




