import os
import logging
import pandas as pd
from typing import Optional

class Data_load:
    """
    A class for reading Data files with robust logging and error handling.

    Attributes
    ----------
    data_dir : str
        The directory where raw data files are stored.
    logger : logging.Logger
        Logger instance for the class.

    Methods
    -------
    read_tsv(filename: str) -> pd.DataFrame:
        Reads a TSV file and returns a pandas DataFrame.
    """

    def __init__(self, data_dir: str = "../data/raw", logger: Optional[logging.Logger] = None):
        """
        Initialize Data reader with a data directory and logger.

        Parameters
        ----------
        data_dir : str
            Path to the directory containing raw data files.
        logger : Optional[logging.Logger]
            Custom logger instance. If None, a default logger is created.
        """
        self.data_dir = data_dir
        self.logger = logger or self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Set up a logger for the TSVReader class.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger("TSVReader")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not logger.hasHandlers():
            logger.addHandler(handler)
        return logger

    def read_tsv(self, filename: str) -> pd.DataFrame:
        """
        Reads a TSV (Tab-Separated Values) file from the data directory.

        Parameters
        ----------
        filename : str
            Name of the TSV file to read.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the TSV data.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        pd.errors.ParserError
            If the file cannot be parsed.
        """
        file_path = os.path.join(self.data_dir, filename)
        self.logger.info(f"Attempting to read TSV file: {file_path}")

        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"TSV file not found: {file_path}")

        try:
            df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
            self.logger.info(f"Successfully read {len(df)} rows from {file_path}")
            return df
        except pd.errors.ParserError as e:
            self.logger.error(f"Parsing error for file {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error reading file {file_path}: {e}")
            raise

# Example usage:
# if __name__ == "__main__":
#     reader = TSVReader()
#     df = reader.read_tsv("sample.tsv")
#     print(df.head())
