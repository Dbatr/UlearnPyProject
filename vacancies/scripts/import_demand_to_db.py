import csv
import os

from vacancies.models import VacancyStats, AvgSalaryStats, BackendStats, BackendAvgSalaryStats

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def import_vacancy_stats():
    csv_file_path = os.path.join(project_root, 'vacancy_query.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            VacancyStats.objects.create(
                year=row['Год'],
                vacancy_count=row['Количество вакансий']
            )


def import_avg_salary_stats():
    csv_file_path = os.path.join(project_root, 'avg_salary_query.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            AvgSalaryStats.objects.create(
                year=row['Год'],
                average_salary=row['Средняя з/п']
            )


def import_backend_stats():
    csv_file_path = os.path.join(project_root, 'backend_query.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            BackendStats.objects.create(
                year=row['Год'],
                backend_vacancy_count=row['Количество вакансий для бэка']
            )


def import_backend_avg_salary_stats():
    csv_file_path = os.path.join(project_root, 'backend_avg_salary_query.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            BackendAvgSalaryStats.objects.create(
                year=row['Год'],
                backend_average_salary=row['Средняя з/п для бэка']
            )


def run():
    import_vacancy_stats()
    import_avg_salary_stats()
    import_backend_stats()
    import_backend_avg_salary_stats()

