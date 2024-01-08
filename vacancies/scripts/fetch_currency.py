import logging
import sys
from datetime import datetime

import requests
import pandas as pd
from lxml.etree import XMLSyntaxError

currency_codes = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]


# Функция для получения значений валют из словаря данных о валютах
def get_currency_values(currency_data_dict):
    values = {}
    for code in currency_codes:

        value = currency_data_dict["Value"].get(code)
        nominal = currency_data_dict["Nominal"].get(code, 1)

        # Рассчитываем курс валюты, учитывая номинал
        values[code] = round(float(value.replace(",", ".")) / float(nominal), 8) if value is not None else None

    return values


# Функция для получения данных о валютах за определенный месяц и год
def fetch_currency_data(month, year):

    # Редактирование записи месяца
    formatted_month = f"0{month}" if month < 10 else str(month)

    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{formatted_month}/{year}"
    #url = f"http://127.0.0.1:8000/scripts/XML_daily.asp?date_req=01/{formatted_month}/{year}"

    try:
        # Чтение данных о валютах из XML и преобразование в DataFrame
        currency_df = pd.read_xml(requests.get(url).text)
        currency_data_dict = currency_df.groupby('CharCode')[['Value', 'Nominal']].first().to_dict()
        # Формирование результата, включая значения валют
        result = {"date": f"{year}-{formatted_month}"}
        result.update(get_currency_values(currency_data_dict))
        return result

    except XMLSyntaxError as e:
        logging.error(f"Error reading XML data: {e}")
        sys.exit(1)



# Функция для получения данных о валютах за заданный период
def generate_currency_data(start_date, end_date):
    start_year, start_month = start_date.year, start_date.month
    end_year, end_month = end_date.year, end_date.month

    # Получение данных о валютах за период от start_date до end_date
    currency_data_list = [fetch_currency_data(month, year) for year in range(start_year, end_year + 1)
                          for month in range(1, 13) if (start_year < year < end_year) or
                          (start_year == year and start_month <= month <= 12) or
                          (end_year == year and 1 <= month <= end_month)]
    return currency_data_list


def run():
    start_date = datetime(2003, 1, 1)  # Начало периода
    end_date = datetime(2023, 12, 31)  # Конец периода

    currency_data_list = generate_currency_data(start_date, end_date)
    df = pd.DataFrame.from_records(currency_data_list)
    df.to_csv('currency.csv', index=False)



