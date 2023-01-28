from typing import Any, Union

import datetime as dt
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from loguru import logger


class CsvReader:
    def __init__(self, file):
        self.file = file
        self.dictionary = ['Комментарий', 'Дата', 'Сумма', 'Категория', 'Счет списания', 'Счет зачисления',
                           'Сумма списания', 'Сумма зачисления', 'Время', 'Описание']

    def read_csv_file(self) -> Union[DataFrame, Exception]:
        """Accepts the file passed to the class for conversion to DataFrame"""
        try:
            return pd.read_csv(self.file, encoding='utf-8', sep=';')
        except UnicodeDecodeError:
            return pd.read_csv(self.file, encoding='ansi', sep=';')
        except Exception as error:
            logger.error(f'An error occurred while trying to read a file: {error}')
            return error

    @staticmethod
    def get_headers(df: Any) -> Union[list, Exception]:
        """Gets a DateFrame to extract the file headers and returns them to a list to check"""
        return df.columns.values.tolist()

    @staticmethod
    def date_pattern_checker(df: DataFrame) -> str:
        date_patterns = ['%d/%m/%y', '%m/%d/%y', '%d.%m.%Y', '%d.%m.%y', '%Y-%m-%d']
        for i in range(len(date_patterns)):
            try:
                dt.datetime.strptime(df.at[0, 'Дата'], date_patterns[i]).date()
                return date_patterns[i]
            except ValueError:
                if i + 1 == len(date_patterns):
                    logger.error(f'No template was found for the date: {df.at[0, "Дата"]}')

    @staticmethod
    def convert_date_to_dt(df: DataFrame, date_pattern: str) -> DataFrame:
        df['Дата'] = pd.to_datetime(df['Дата'], format=date_pattern).dt.date
        df['Время'] = pd.to_datetime(df['Время']).dt.time
        return df

    @staticmethod
    def filtered_df_by_datetime(df: Any) -> DataFrame:
        """Retrieves transactions from DataFrame with future date and time only'"""
        datetime_now = dt.datetime.now()
        date_now = datetime_now.date()
        time_now = datetime_now.time()
        df = df[(df['Дата'] >= date_now) & (df['Время'] > time_now)]
        return df

    @staticmethod
    def change_nan_on_none(df: DataFrame) -> DataFrame:
        return df.replace({np.nan: None})

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

    def run_test(self) -> dict or str:
        """Runs all the necessary functions and contains a check"""
        # Read file
        df = self.read_csv_file()
        logger.info(f'\n{df}')

        # Check headers
        check = self.check_keys(CsvReader.get_headers(df))
        if check is not None:
            logger.error(f'Title not found: {check}')
            return f'Произошла ошибка при проверке файла. Заголовок {check} не найден в файле.'
        logger.info('The headers have been successfully checked')
        # Check date format in file
        pattern = CsvReader.date_pattern_checker(df)
        logger.info(f'Date format: {pattern}')

        # Convert type in column date
        converted_df = CsvReader.convert_date_to_dt(df, pattern)
        logger.info(f'\n{converted_df}')

        # Filter df >= datetime now
        filtered_df = CsvReader.filtered_df_by_datetime(converted_df)
        logger.info(f'\n{filtered_df}')
        return CsvReader.df_to_dict(CsvReader.change_nan_on_none(filtered_df))
