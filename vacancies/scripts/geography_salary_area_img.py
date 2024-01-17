import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings


# python manage.py runscript geography_salary_area_img -v2
def create_salary_area_graph(df, title, img_path):
    fig, ax = plt.subplots()
    cities = np.arange(len(df['Город']))
    ax.barh(y=cities, width=df['Уровень зарплат по городам'], height=0.4, label='Уровень зарплат')
    ax.set_title(title)
    ax.set_yticks(cities)
    ax.set_yticklabels(df['Город'], fontsize=6)
    ax.legend()
    ax.grid(axis='x')

    fig.savefig(img_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {os.path.basename(img_path)}")


def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса
    query_all = """
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

    df_all = pd.read_sql_query(query_all, conn)

    # Выполнение второго SQL-запроса
    query_backend = """
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

    df_backend = pd.read_sql_query(query_backend, conn)

    # Закрытие соединения с базой данных
    conn.close()

    # Создание графика для всех вакансий
    create_salary_area_graph(df_all, 'Уровень зарплат по городам',
                             os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'geography_salary_area_all.png'))

    # Создание графика для вакансий бэка
    create_salary_area_graph(df_backend, 'Уровень зарплат по городам для Backend-программиста',
                             os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'geography_salary_area_backend.png'))