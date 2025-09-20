
from main import os, sys, _setup_logger , Optional, logging, app_logger, pd
from pathlib import Path

# log = _setup_logger

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

    def __init__(self, data_dir: Optional[Path] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize Data reader with a data directory and logger.

        Parameters
        ----------
        data_dir : str
            Path to the directory containing raw data files.
        logger : Optional[logging.Logger]
            Custom logger instance. If None, a default logger is created.
        """
        if data_dir:
            self.data_dir = data_dir
        else:
            project_root = Path(__file__).resolve().parent.parent
            self.data_dir = os.path.join(project_root,"data/raw")

        self.logger = logger or app_logger

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
app_logger.info(f"execuiting data_load.py as <<<{__name__}>>>")
if __name__ == "__main__":
    reader = Data_load()
    print(reader.read_tsv("drugLibTest_raw.tsv").head())