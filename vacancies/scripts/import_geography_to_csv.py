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


def run():
    # Сохранение результатов запроса в CSV-файл
    save_query_results_to_csv(salary_area, 'salary_area.csv')
    save_query_results_to_csv(dolya_area, 'dolya_area.csv')
    save_query_results_to_csv(salary_area_backend, 'salary_area_backend.csv')
    save_query_results_to_csv(dolya_area_backend, 'dolya_area_backend.csv')