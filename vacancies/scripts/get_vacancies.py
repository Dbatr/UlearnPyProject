# python manage.py runscript get_vacancies -v2

import requests
from datetime import datetime
import re

currency_mapping = {
        "AZN": "Манаты",
        "BYR": "Белорусские рубли",
        "EUR": "Евро",
        "GEL": "Грузинский лари",
        "KGS": "Киргизский сом",
        "KZT": "Тенге",
        "RUR": "Рубли",
        "UAH": "Гривны",
        "USD": "Доллары",
        "UZS": "Узбекский сум"
}

nalogi = {
    "true": "(Без вычета налогов)",
    "false": "(С вычетом налогов)"
}


def clean_html(text):
    # Удаление HTML-тегов
    clean_text = re.sub('<.*?>', '', text)
    # Замена HTML-кодов символов
    clean_text = re.sub('&quot;', '"', clean_text)
    clean_text = re.sub('&amp;', '&', clean_text)
    clean_text = re.sub('&lt;', '<', clean_text)
    clean_text = re.sub('&gt;', '>', clean_text)
    clean_text = re.sub('&nbsp;', ' ', clean_text)
    clean_text = re.sub('&copy;', '©', clean_text)
    clean_text = re.sub('&reg;', '®', clean_text)
    return clean_text


def get_vacancy_details(vacancy_id):
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        description = data.get("description", "")

        # Используем функцию clean_html для удаления HTML-тегов и HTML-кодов символов
        description = clean_html(description)

        key_skills = data.get("key_skills", [])
        key_skills = [skill.get("name", "") for skill in key_skills]

        return description, key_skills
    else:
        print(
            f"Failed to get description and key skills for vacancy ID {vacancy_id}. Status code: {response.status_code}")
        return "", []


def calculate_average_salary(salary_from, salary_to):
    salary_from = salary_from or 0
    salary_to = salary_to or 0

    if salary_from != 0 and salary_to != 0:
        return (salary_from + salary_to) / 2
    elif salary_from == 0 and salary_to != 0:
        return salary_to
    elif salary_from != 0 and salary_to == 0:
        return salary_from


def format_published_date(published_at):
    # Преобразование строки в формат datetime
    date_object = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S%z")
    # Форматирование даты в нужный вид
    formatted_date = date_object.strftime("%d.%m.%Y")
    return formatted_date


def get_vacancy_info(vacancy):
    vacancy_id = vacancy.get("id")
    vacancy_title = vacancy.get("name")
    vacancy_url = vacancy.get("alternate_url")
    company_name = vacancy.get("employer", {}).get("name")
    region_name = vacancy.get("area", {}).get("name")
    published_at = vacancy.get("published_at")

    published_at = format_published_date(published_at)

    salary_info = vacancy.get("salary", {})
    if salary_info:
        salary_from = salary_info.get("from", 0)
        salary_to = salary_info.get("to", 0)
        currency = salary_info.get("currency")
        gross = salary_info.get("gross")

    else:
        salary_from = salary_to = 0
        currency = gross = None

    average_salary = calculate_average_salary(salary_from, salary_to)
    # Замена кода валюты на полное название
    currency = currency_mapping.get(currency, currency)

    return [
        vacancy_id, vacancy_url, vacancy_title, company_name, average_salary,
        currency, gross, region_name, published_at
            ]


def run():
    keywords = ['backend', 'Backend', 'бэкэнд', 'back end']
    url = "https://api.hh.ru/vacancies"
    today = datetime.now().replace(hour=0, minute=0, second=0)
    params = {
        "text": " AND ".join(keywords),
        "date_from": today.isoformat(),
        "per_page": 10,
        "order_by": "publication_time"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])

        vacancy_list = []

        for vacancy in vacancies:
            vacancy_info = get_vacancy_info(vacancy)

            vacancy_id = vacancy.get("id")
            description, key_skills = get_vacancy_details(vacancy_id)

            vacancy_info.append(description)
            vacancy_info.append(key_skills)

            vacancy_list.append(vacancy_info)

        return vacancy_list

    else:
        return []