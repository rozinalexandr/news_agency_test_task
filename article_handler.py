import pandas as pd
import shutil
import os


class ArticleHandler:
    def __init__(self, raw_data_file_name: str):
        self._raw_data_file_name = raw_data_file_name
        self._path_to_raw_data_dir = "raw_data/"
        self._path_to_processed_data_dir = "processed_data/"

    def _copy_raw_data_file(self):
        if not os.path.exists(self._path_to_processed_data_dir):
            os.mkdir(self._path_to_processed_data_dir)

        if not os.path.exists(self._path_to_processed_data_dir + self._raw_data_file_name):
            original = self._path_to_raw_data_dir + self._raw_data_file_name
            target = self._path_to_processed_data_dir + self._raw_data_file_name
            shutil.copyfile(original, target)

    def _read_csv_file(self):
        return pd.read_csv(self._path_to_processed_data_dir + self._raw_data_file_name)

    def _save_csv_file(self, df):
        df.to_csv(self._path_to_processed_data_dir + self._raw_data_file_name, index=False)

    def drop_na_rows(self, column_name: list):
        self._copy_raw_data_file()

        df = self._read_csv_file()
        df.dropna(subset=column_name, inplace=True)
        self._save_csv_file(df)

    def drop_duplicated_rows(self, column_name: list):
        self._copy_raw_data_file()

        df = self._read_csv_file()
        df.drop_duplicates(subset=column_name, inplace=True)
        self._save_csv_file(df)
