import csv
from django.db import connection

def save_query_results_to_csv(query, filename):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)

# Ваш запрос
vacancy_query = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        COUNT(*) AS 'Количество вакансий'
    FROM vacancies
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4) DESC
"""

# Запрос для средней зарплаты
avg_salary_query = """
            SELECT
                SUBSTR(published_at, 1, 4) AS 'Год',
                ROUND(AVG(salary), 2) AS 'Средняя з/п'
            FROM processed_vacancies
            GROUP BY SUBSTR(published_at, 1, 4)
            ORDER BY SUBSTR(published_at, 1, 4) DESC
        """
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


def run():
    # Сохранение результатов запроса в CSV-файл
    save_query_results_to_csv(vacancy_query, 'vacancy_query.csv')
    save_query_results_to_csv(avg_salary_query, 'avg_salary_query.csv')
    save_query_results_to_csv(backend_query, 'backend_query.csv')
    save_query_results_to_csv(backend_avg_salary_query, 'backend_avg_salary_query.csv')