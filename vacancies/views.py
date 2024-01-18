import sqlite3
import csv
import threading
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.core.cache import cache
from vacancies.scripts import get_vacancies

# def csvread():
#     connection = sqlite3.connect('db.sqlite3')
#     time_start = time.time()
#     with open('vacancies.csv', encoding='utf-8-sig') as r_file:
#         file_reader = csv.reader(r_file, delimiter=",")
#         i = 0
#         next(file_reader)
#         for row in file_reader:
#             connection.execute("insert into vacancies(name,key_skills,salary_from,salary_to,salary_currency,area_name,published_at) values(?,?,?,?,?,?,?)" , row)
#             i+=1
#             if i % 1000000 == 0:
#                 print(time.time() - time_start , i)
#                 connection.commit()
#     # Сохраняем изменения и закрываем соединение
#     connection.commit()
#     connection.close()
#     print("last: ", time.time()-time_start , i)


def index(request):
    # Отображаем шаблон
    return render(request, 'vacancies/index.html')


def execute_sql_query(query, key, cache_time=3600):
    cached_result = cache.get(key)

    if cached_result is not None:
        result = cached_result
    else:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        cache.set(key, result, cache_time)

    return result


# Страница востребованности
def demand(request):
    # Запрос для статистики по количеству вакансий
    vacancy_query = """
            SELECT
                SUBSTR(published_at, 1, 4) AS 'Год',
                COUNT(*) AS 'Количество вакансий'
            FROM vacancies
            GROUP BY SUBSTR(published_at, 1, 4)
            ORDER BY SUBSTR(published_at, 1, 4) DESC
        """
    result = execute_sql_query(vacancy_query, 'vacancy_stats')

    # Запрос для средней зарплаты
    avg_salary_query = """
            SELECT
                SUBSTR(published_at, 1, 4) AS 'Год',
                ROUND(AVG(salary), 2) AS 'Средняя з/п'
            FROM processed_vacancies
            GROUP BY SUBSTR(published_at, 1, 4)
            ORDER BY SUBSTR(published_at, 1, 4) DESC
        """
    avg_salary_result = execute_sql_query(avg_salary_query, 'avg_salary_stats')

    # Запрос для Backend-программистов
    backend_query = """
            SELECT
                SUBSTR(published_at, 1, 4) AS 'Год',
                COUNT(*) AS 'Количество вакансий для бэка'
            FROM vacancies
            WHERE 
                name LIKE '%backend%'
                OR name LIKE '%Backend-программист%'
                OR name LIKE '%бэкэнд%'
                OR name LIKE '%бэкенд%'
                OR name LIKE '%бекенд%'
                OR name LIKE '%бекэнд%'
                OR name LIKE '%back end%'
                OR name LIKE '%бэк энд%'
                OR name LIKE '%бэк енд%'
                OR name LIKE '%django%'
                OR name LIKE '%flask%'
                OR name LIKE '%laravel%'
                OR name LIKE '%yii%'
                OR name LIKE '%symfony%'
            GROUP BY SUBSTR(published_at, 1, 4)
            ORDER BY SUBSTR(published_at, 1, 4) DESC
        """
    backend_result = execute_sql_query(backend_query, 'backend_stats')

    # Запрос для средней зарплаты Backend-программистов
    backend_avg_salary_query = """
            SELECT
                SUBSTR(published_at, 1, 4) AS 'Год',
                ROUND(AVG(salary), 2) AS 'Средняя з/п для бэка'
            FROM processed_vacancies
            WHERE 
                name LIKE '%backend%'
                OR name LIKE '%Backend-программист%'
                OR name LIKE '%бэкэнд%'
                OR name LIKE '%бэкенд%'
                OR name LIKE '%бекенд%'
                OR name LIKE '%бекэнд%'
                OR name LIKE '%back end%'
                OR name LIKE '%бэк энд%'
                OR name LIKE '%бэк енд%'
                OR name LIKE '%django%'
                OR name LIKE '%flask%'
                OR name LIKE '%laravel%'
                OR name LIKE '%yii%'
                OR name LIKE '%symfony%'
            GROUP BY SUBSTR(published_at, 1, 4)
            ORDER BY SUBSTR(published_at, 1, 4) DESC
        """
    backend_avg_salary_result = execute_sql_query(backend_avg_salary_query, 'backend_avg_salary_stats')

    # Передаем результаты запросов в контекст шаблона
    context = {
        'vacancy_stats': result,
        'avg_salary_stats': avg_salary_result,
        'backend_stats': backend_result,
        'backend_avg_salary_stats': backend_avg_salary_result,
    }

    # Отображаем шаблон
    return render(request, 'vacancies/demand.html', context)


def geography(request):
    # Запрос для уровня зарплат по городам
    salary_area = """
                    SELECT
                        area_name AS 'Город',
                        ROUND(AVG(salary), 2) AS 'Уровень зарплат по городам'
                    FROM processed_vacancies
                    GROUP BY area_name
                    HAVING CAST(COUNT(*) AS REAL) >= 
                    ((SELECT COUNT(*) FROM processed_vacancies)/100)
                    ORDER BY ROUND(AVG(salary),2) DESC
                    LIMIT 15
                """
    result = execute_sql_query(salary_area, 'salary_area')

    # Запрос для доли вакансий по городам
    dolya_area = """
                        SELECT
                            area_name AS 'Город',
                            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 2) AS 'Доля вакансий в %'
                        FROM vacancies
                        GROUP BY area_name
                        ORDER BY COUNT(*) DESC
                        LIMIT 15
                    """
    dolya_area_result = execute_sql_query(dolya_area, 'dolya_area')

    # Запрос для уровня зарплат по городам для бэкендера
    salary_area_backend = """
                        SELECT
                        area_name AS 'Город',
                        ROUND(AVG(salary), 2) AS 'Уровень зарплат по городам'
                    FROM processed_vacancies
                    WHERE
                        (name LIKE '%backend%'
                        OR name LIKE '%Backend-программист%'
                        OR name LIKE '%бэкэнд%'
                        OR name LIKE '%бэкенд%'
                        OR name LIKE '%бекенд%'
                        OR name LIKE '%бекэнд%'
                        OR name LIKE '%back end%'
                        OR name LIKE '%бэк энд%'
                        OR name LIKE '%бэк енд%'
                        OR name LIKE '%django%'
                        OR name LIKE '%flask%'
                        OR name LIKE '%laravel%'
                        OR name LIKE '%yii%'
                        OR name LIKE '%symfony%')
                    GROUP BY area_name
                    ORDER BY ROUND(AVG(salary),2) DESC
                    LIMIT 15
                    """
    backend_result = execute_sql_query(salary_area_backend, 'salary_area_backend')

    # Запрос для доли вакансий по городам для бэкендера
    dolya_area_backend = """
                            SELECT
                                area_name AS 'Город',
                                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 3) AS 'Доля вакансий в %'
                            FROM vacancies
                            WHERE
                                (name LIKE '%backend%'
                                OR name LIKE '%Backend-программист%'
                                OR name LIKE '%бэкэнд%'
                                OR name LIKE '%бэкенд%'
                                OR name LIKE '%бекенд%'
                                OR name LIKE '%бекэнд%'
                                OR name LIKE '%back end%'
                                OR name LIKE '%бэк энд%'
                                OR name LIKE '%бэк енд%'
                                OR name LIKE '%django%'
                                OR name LIKE '%flask%'
                                OR name LIKE '%laravel%'
                                OR name LIKE '%yii%'
                                OR name LIKE '%symfony%')
                            GROUP BY area_name
                            ORDER BY COUNT(*) DESC
                            LIMIT 15
                        """
    dolya_area_backend_result = execute_sql_query(dolya_area_backend, 'dolya_area_backend')

    # Передаем результаты запросов в контекст шаблона
    context = {
        'salary_area': result,
        'dolya_area': dolya_area_result,
        'salary_area_backend': backend_result,
        'dolya_area_backend': dolya_area_backend_result
    }

    # Отображаем шаблон
    return render(request, 'vacancies/geography.html', context)


def skills(request):
    csv_file_path = 'all_skills.csv'
    backend_csv_file_path = 'backend_skills.csv'

    # Read main CSV file and extract data
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        skills_data = list(reader)

    unique_years = sorted(set(row['Year'] for row in skills_data), reverse=True)

    with open(backend_csv_file_path, 'r', encoding='utf-8') as backend_file:
        backend_reader = csv.DictReader(backend_file)
        backend_skills_data = list(backend_reader)

    unique_backend_years = sorted(set(row['Year'] for row in backend_skills_data), reverse=True)

    context = {
        'skills_data': skills_data,
        'unique_years': unique_years,
        'backend_skills_data': backend_skills_data,
        'unique_backend_years': unique_backend_years,
    }

    # Render the template for skills
    return render(request, 'vacancies/skills.html', context)


def last_vacancies(request):
    vacancies = get_vacancies.run()
    return render(request, 'vacancies/last_vacancies.html', {'vacancies': vacancies})