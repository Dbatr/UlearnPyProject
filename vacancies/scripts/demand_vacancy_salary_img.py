# python manage.py runscript demand_vacancy_salary_img -v2

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings


def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса
    query_avg_salary = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        ROUND(AVG(salary), 2) AS 'Средняя з/п'
    FROM processed_vacancies
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_avg_salary = pd.read_sql_query(query_avg_salary, conn)

    # Выполнение второго SQL-запроса
    query_avg_salary_backend = """
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
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_avg_salary_backend = pd.read_sql_query(query_avg_salary_backend, conn)

    # Закрытие соединения с базой данных
    conn.close()

    # Создание графика для средней зарплаты
    fig_avg_salary, ax_avg_salary = plt.subplots()
    ax_avg_salary.plot(df_avg_salary['Год'], df_avg_salary['Средняя з/п'], label='Средняя зарплата', marker='o')
    ax_avg_salary.set_title('Средняя зарплата по годам для всех вакансий')
    ax_avg_salary.legend()
    ax_avg_salary.grid(axis='y')

    # Поворот меток оси x
    plt.xticks(rotation=60)

    # Сохранение графика для средней зарплаты как изображения
    img_path_avg_salary = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'demand_avg_salary.png')
    fig_avg_salary.savefig(img_path_avg_salary)
    plt.close(fig_avg_salary)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")

    # Создание графика для средней зарплаты бэка
    fig_avg_salary_backend, ax_avg_salary_backend = plt.subplots()
    ax_avg_salary_backend.plot(df_avg_salary_backend['Год'], df_avg_salary_backend['Средняя з/п для бэка'],
                               label='Средняя зарплата', marker='o')
    ax_avg_salary_backend.set_title('Средняя зарплата по годам для Backend-программиста')
    ax_avg_salary_backend.legend()
    ax_avg_salary_backend.grid(axis='y')

    # Поворот меток оси x
    plt.xticks(rotation=60)

    # Сохранение графика для средней зарплаты бэка как изображения
    img_path_avg_salary_backend = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img',
                                               'demand_avg_salary_backend.png')
    fig_avg_salary_backend.savefig(img_path_avg_salary_backend)
    plt.close(fig_avg_salary_backend)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")
