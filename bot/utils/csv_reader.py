from typing import Any, Union

import datetime as dt
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame


class CsvReader:
    def __init__(self, file):
        self.file = file
        self.dictionary = ['Описание', 'Дата', 'Сумма', 'Категория', 'Счет', 'Время']

    def read_csv_file(self) -> Union[DataFrame, Exception]:
        """Accepts the file passed to the class for conversion to DataFrame"""
        try:
            return pd.read_csv(self.file, encoding='utf-8', sep=';')
        except UnicodeDecodeError:
            return pd.read_csv(self.file, encoding='ansi', sep=';')
        except Exception as error:
            # TODO: log
            return error

    @staticmethod
    def get_headers(df: Any) -> Union[list, Exception]:
        """Gets a DateFrame to extract the file headers and returns them to a list to check"""
        try:
            return df.columns.values.tolist()
        except Exception as error:
            # TODO: log
            return error

    @staticmethod
    def filtered_df_by_datetime(df: Any) -> DataFrame:
        """Retrieves transactions from DataFrame with future date and time only'"""
        datetime_now = dt.datetime.now()
        date_str = datetime_now.strftime('%d/%m/%y')
        time_str = datetime_now.strftime('%H:%M')
        filtered = df[(df['Дата'] >= date_str) & (df['Время'] > time_str)]

        change_nan_on_none = filtered.replace({np.nan: None})
        return change_nan_on_none

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
        return CsvReader.df_to_dict(CsvReader.filtered_df_by_datetime(df))
