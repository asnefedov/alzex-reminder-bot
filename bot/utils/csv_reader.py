from typing import Any

import pandas as pd
from pandas.core.frame import DataFrame


class CsvReader:
    def __init__(self, file):
        self.file = file
        self.dictionary = ['Описание', 'Дата', 'Сумма', 'Категория', 'Счет', 'Статус', 'Время']

    def read_csv_file(self) -> DataFrame:
        """Accepts the file passed to the class for conversion to DataFrame"""
        try:
            return pd.read_csv(self.file, encoding='utf-8', sep=';')
        except UnicodeDecodeError:
            return pd.read_csv(self.file, encoding='ansi', sep=';')
        except Exception as error:
            print(f'Произошла ошибка при чтении файла: {error}')

    @staticmethod
    def get_headers(df: Any) -> list:
        """Gets a DateFrame to extract the file headers and returns them to a list to check"""
        return df.columns.values.tolist()

    @staticmethod
    def filtered_df_by_status(df: Any) -> DataFrame:
        """Retrieves transactions from the DataFrame only with the status 'Unconfirmed'"""
        filtered = df[(df['Статус'].isnull())]
        return filtered

    @staticmethod
    def df_to_dict(df: Any) -> list:
        """Converts a DataFrame to a dictionary for easy entry into a database"""
        df: DataFrame
        return df.to_dict(orient='records')

    def check_keys(self, headers: list) -> None or str:
        """Checks if the file contains all the required headers"""
        for header in self.dictionary:
            if header not in headers:
                return header

    def run(self) -> dict or str:
        """Runs all the necessary functions and contains a check"""
        df = self.read_csv_file()
        check = self.check_keys(CsvReader.get_headers(df))
        if check is not None:
            return f'Произошла ошибка при проверке файла. Заголовок {check} не найден в файле.'
        return CsvReader.df_to_dict(CsvReader.filtered_df_by_status(df))
