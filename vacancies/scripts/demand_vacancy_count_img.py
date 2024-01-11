import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса
    query_all = """
    SELECT
        SUBSTR(published_at, 1, 4) AS 'Год',
        COUNT(*) AS 'Количество вакансий'
    FROM vacancies
    GROUP BY SUBSTR(published_at, 1, 4)
    ORDER BY SUBSTR(published_at, 1, 4)
    """

    df_all = pd.read_sql_query(query_all, conn)

    # Выполнение второго SQL-запроса
    query_backend = """
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
    ORDER BY SUBSTR(published_at, 1, 4) 
    """

    df_backend = pd.read_sql_query(query_backend, conn)

    # Закрытие соединения с базой данных
    conn.close()

    # Создание графика для всех вакансий
    fig_all, ax_all = plt.subplots()
    years_all = np.arange(len(df_all['Год']))
    ax_all.bar(x=years_all, height=df_all['Количество вакансий'], width=0.4, label='Количество вакансий')
    ax_all.set_title('Количество всех вакансий по годам')
    ax_all.set_xticks(years_all)
    ax_all.set_xticklabels(df_all['Год'], rotation=90, ha='center')
    ax_all.legend()
    ax_all.grid(axis='y')

    # Сохранение графика для всех вакансий как изображения
    img_path_all = os.path.join('vacancies_all.png')
    fig_all.savefig(img_path_all)
    plt.close(fig_all)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")

    # Создание графика для вакансий бэка
    fig_backend, ax_backend = plt.subplots()
    years_backend = np.arange(len(df_backend['Год']))
    ax_backend.bar(x=years_backend, height=df_backend['Количество вакансий для бэка'], width=0.4, label='Количество вакансий')
    ax_backend.set_title('Количество вакансий по годам для Backend-программиста')
    ax_backend.set_xticks(years_backend)
    ax_backend.set_xticklabels(df_backend['Год'], rotation=90, ha='center')
    ax_backend.legend()
    ax_backend.grid(axis='y')

    # Сохранение графика для вакансий бэка как изображения
    img_path_backend = os.path.join('vacancies_backend.png')
    fig_backend.savefig(img_path_backend)
    plt.close(fig_backend)  # Закрыть график, чтобы освободить ресурсы
    print("Saved")