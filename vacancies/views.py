import os
import sqlite3
import csv
import threading
import time
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.core.cache import cache

from vacancies.models import *
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


# Страница востребованности
def demand(request):
    result = VacancyStats.objects.all()
    avg_salary_result = AvgSalaryStats.objects.all()
    backend_result = BackendStats.objects.all()
    backend_avg_salary_result = BackendAvgSalaryStats.objects.all()

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

    result = SalaryArea.objects.all()
    dolya_area_result = DolyaArea.objects.all()
    backend_result = SalaryAreaBackend.objects.all()
    dolya_area_backend_result = DolyaAreaBackend.objects.all()

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
    # Получаем абсолютный путь к корню проекта
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Формируем абсолютный путь к файлу 'all_skills.csv'
    csv_file_path = os.path.join(project_root, 'all_skills.csv')

    # Формируем абсолютный путь к файлу 'backend_skills.csv'
    backend_csv_file_path = os.path.join(project_root, 'backend_skills.csv')

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