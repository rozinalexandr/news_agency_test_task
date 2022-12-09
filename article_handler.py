import pandas as pd
import shutil
import os


class ArticleHandler:
    """
    This class does a basic cleanup of the dataset of empty data. Using the 'raw' data obtained after parsing, this
    class removes empty rows and duplicates.
    This class uses a copy of 'raw' data file, so you will always have the original file with the raw data, as well as
    the processed file.
    """
    def __init__(self, raw_data_file_name: str):
        """
        :param raw_data_file_name: Name of a .csv file with raw data
        :param path_to_raw_data_dir: Path to directory, where raw data is stored
        :param path_to_processed_data_dir: Path to directory, where processed data is stored
        """
        self._raw_data_file_name = raw_data_file_name
        self._path_to_raw_data_dir = "raw_data/"
        self._path_to_processed_data_dir = "processed_data/"

    def _copy_raw_data_file(self):
        """
        This method copies the raw dataset and moves it to a new directory where the processed data is stored.
        If there is no directory, this method will create it.
        If there is no dataset in processed_data directory, this method will copy the raw data and paste it into
        processed_data directory.
        Otherwise, it will not make any changes.
        """
        if not os.path.exists(self._path_to_processed_data_dir):
            os.mkdir(self._path_to_processed_data_dir)

        if not os.path.exists(self._path_to_processed_data_dir + self._raw_data_file_name):
            original = self._path_to_raw_data_dir + self._raw_data_file_name
            target = self._path_to_processed_data_dir + self._raw_data_file_name
            shutil.copyfile(original, target)

    def _read_csv_file(self):
        """
        Method, that reads .csv file
        :return: Pandas DataFrame of required data
        """
        return pd.read_csv(self._path_to_processed_data_dir + self._raw_data_file_name)

    def _save_csv_file(self, df):
        """
        Method saves Pandas DataFrame into .csv format
        :param df: Pandas DataFrame, which is needed to be saved into .csv format
        """
        df.to_csv(self._path_to_processed_data_dir + self._raw_data_file_name, index=False)

    def drop_na_rows(self, column_name: list):
        """
        Method drops rows with no information. Method saves received dataset to the initial file.
        :param column_name: List of columns, where you want to drop Nan values
        """
        self._copy_raw_data_file()

        df = self._read_csv_file()
        df.dropna(subset=column_name, inplace=True)
        self._save_csv_file(df)

    def drop_duplicated_rows(self, column_name: list):
        """
        Method drops duplicated rows by a specific column. Method saves received dataset to the initial file.
        :param column_name: List of columns, where you want to drop duplicated values
        """
        self._copy_raw_data_file()

        df = self._read_csv_file()
        df.drop_duplicates(subset=column_name, inplace=True)
        self._save_csv_file(df)
