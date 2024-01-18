# python manage.py runscript get_vacancies -v2

import requests
from datetime import datetime
import re


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
        return description, key_skills
    else:
        print(
            f"Failed to get description and key skills for vacancy ID {vacancy_id}. Status code: {response.status_code}")
        return "", []


def get_vacancy_info(vacancy):
    vacancy_id = vacancy.get("id")
    vacancy_title = vacancy.get("name")
    vacancy_url = vacancy.get("alternate_url")
    company_name = vacancy.get("employer", {}).get("name")
    region_name = vacancy.get("area", {}).get("name")
    published_at = vacancy.get("published_at")

    salary_info = vacancy.get("salary", {})
    if salary_info:
        salary_from = salary_info.get("from", 0)
        salary_to = salary_info.get("to", 0)
        currency = salary_info.get("currency")
        gross = salary_info.get("gross")

    else:
        salary_from = salary_to = 0
        currency = gross = None
    return [vacancy_id, vacancy_url, vacancy_title, company_name, salary_from, salary_to, currency, gross, region_name, published_at
            ]


def run():
    keywords = ['backend', 'Backend-программист', 'бэкэнд', 'back end']
    url = "https://api.hh.ru/vacancies"
    today = datetime.now().replace(hour=0, minute=0, second=0)
    params = {
        "text": " OR ".join(keywords),
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