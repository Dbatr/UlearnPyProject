import sqlite3
import csv
import threading
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.core.cache import cache

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
            ORDER BY SUBSTR(published_at, 1, 4)
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
