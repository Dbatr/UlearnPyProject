import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings


# python manage.py runscript geography_salary_area_img -v2
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
    fig_all, ax_all = plt.subplots()
    cities_all = np.arange(len(df_all['Город']))
    ax_all.barh(y=cities_all, width=df_all['Уровень зарплат по городам'], height=0.4, label='Уровень зарплат')
    ax_all.set_title('Уровень зарплат по городам')
    ax_all.set_yticks(cities_all)
    ax_all.set_yticklabels(df_all['Город'], fontsize=6)
    ax_all.legend()
    ax_all.grid(axis='x')

    # Сохранение графика для всех вакансий как изображения
    img_path_all = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'salary_area_all.png')
    fig_all.savefig(img_path_all, bbox_inches='tight')
    plt.close(fig_all)
    print("Saved")

    # Создание графика для вакансий бэка
    fig_backend, ax_backend = plt.subplots()
    cities_backend = np.arange(len(df_backend['Город']))
    ax_backend.barh(y=cities_backend, width=df_backend['Уровень зарплат по городам'], height=0.4, label='Уровень зарплат')
    ax_backend.set_title('Уровень зарплат по городам для Backend-программиста')
    ax_backend.set_yticks(cities_backend)
    ax_backend.set_yticklabels(df_backend['Город'], fontsize=6)
    ax_backend.legend()
    ax_backend.grid(axis='x')

    # Сохранение графика для вакансий бэка как изображения
    img_path_backend = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'salary_area_backend.png')
    fig_backend.savefig(img_path_backend, bbox_inches='tight')
    plt.close(fig_backend)
    print("Saved")
