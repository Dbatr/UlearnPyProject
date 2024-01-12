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
    years_avg_salary = np.arange(len(df_avg_salary['Год']))
    ax_avg_salary.bar(x=years_avg_salary, height=df_avg_salary['Средняя з/п'], width=0.4, label='Средняя зарплата')
    ax_avg_salary.set_title('Средняя зарплата по годам')
    ax_avg_salary.set_xticks(years_avg_salary)
    ax_avg_salary.set_xticklabels(df_avg_salary['Год'], rotation=90, ha='center')
    ax_avg_salary.legend()
    ax_avg_salary.grid(axis='y')

    # Сохранение графика для средней зарплаты как изображения
    img_path_avg_salary = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'avg_salary.png')
    fig_avg_salary.savefig(img_path_avg_salary)
    plt.close(fig_avg_salary)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")

    # Создание графика для средней зарплаты бэка
    fig_avg_salary_backend, ax_avg_salary_backend = plt.subplots()
    years_avg_salary_backend = np.arange(len(df_avg_salary_backend['Год']))
    ax_avg_salary_backend.bar(x=years_avg_salary_backend, height=df_avg_salary_backend['Средняя з/п для бэка'], width=0.4, label='Средняя зарплата для бэка')
    ax_avg_salary_backend.set_title('Средняя зарплата для Backend-программиста по годам')
    ax_avg_salary_backend.set_xticks(years_avg_salary_backend)
    ax_avg_salary_backend.set_xticklabels(df_avg_salary_backend['Год'], rotation=90, ha='center')
    ax_avg_salary_backend.legend()
    ax_avg_salary_backend.grid(axis='y')

    # Сохранение графика для средней зарплаты бэка как изображения
    img_path_avg_salary_backend = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'avg_salary_backend.png')
    fig_avg_salary_backend.savefig(img_path_avg_salary_backend)
    plt.close(fig_avg_salary_backend)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")
