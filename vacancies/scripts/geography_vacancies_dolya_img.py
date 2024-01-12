import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings


# python manage.py runscript geography_vacancies_dolya_img -v2
def run():
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')  # Используйте имя вашей базы данных

    # Выполнение первого SQL-запроса (все вакансии)
    query_all = """
        SELECT
            area_name AS 'Город',
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 2) AS 'Доля вакансий в %'
        FROM vacancies
        GROUP BY area_name
        ORDER BY COUNT(*) DESC
        LIMIT 15
    """

    df_all = pd.read_sql_query(query_all, conn)

    # Выполнение второго SQL-запроса (вакансии по backend)
    query_backend = """
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

    df_backend = pd.read_sql_query(query_backend, conn)

    # Закрытие соединения с базой данных
    conn.close()

    # Создание круговой диаграммы для всех вакансий
    fig_all, ax_all = plt.subplots()
    ax_all.pie(df_all['Доля вакансий в %'], labels=df_all['Город'], startangle=90, autopct='%1.1f%%', pctdistance=0.85)
    ax_all.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax_all.set_title('Доля вакансий в % по городам (все вакансии)')

    # Сохранение диаграммы для всех вакансий как изображения
    img_path_all = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'pie_all.png')
    fig_all.savefig(img_path_all)
    plt.close(fig_all)
    print("Saved")

    # Создание круговой диаграммы для вакансий бэка
    fig_backend, ax_backend = plt.subplots()
    ax_backend.pie(df_backend['Доля вакансий в %'], labels=df_backend['Город'], autopct='%1.1f%%', startangle=90)
    ax_backend.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax_backend.set_title('Доля вакансий в % по городам (вакансии по backend)')

    # Сохранение диаграммы для вакансий бэка как изображения
    img_path_backend = os.path.join(settings.BASE_DIR, 'vacancies', 'static', 'vacancies', 'img', 'pie_backend.png')
    fig_backend.savefig(img_path_backend)
    plt.close(fig_backend)
    print("Saved")
