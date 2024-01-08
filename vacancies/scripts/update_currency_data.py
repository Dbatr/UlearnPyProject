import pandas as pd

from vacancies.models import Currency

def save_currency_data_to_database():
    # Чтение данных из CSV файла
    df = pd.read_csv('currency.csv')

    # Преобразование DataFrame в список словарей
    currency_data_list = df.to_dict(orient='records')

    for currency_data in currency_data_list:
        currency = Currency(date=currency_data.get('date'), byr=currency_data.get('BYR'), usd=currency_data.get('USD'),
                            eur=currency_data.get('EUR'), kzt=currency_data.get('KZT'),
                            uah=currency_data.get('UAH'), azn=currency_data.get('AZN'),
                            kgs=currency_data.get('KGS'), uzs=currency_data.get('UZS'),
                            gel=currency_data.get('GEL'))
        currency.save()

def run():
    save_currency_data_to_database()