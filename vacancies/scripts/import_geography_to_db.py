import csv
import os
from vacancies.models import SalaryArea, DolyaArea, SalaryAreaBackend, DolyaAreaBackend

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def import_salary_area():
    csv_file_path = os.path.join(project_root, 'salary_area.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            SalaryArea.objects.create(
                area_name=row['Город'],
                average_salary=row['Уровень зарплат по городам']
            )


def import_dolya_area():
    csv_file_path = os.path.join(project_root, 'dolya_area.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            DolyaArea.objects.create(
                area_name=row['Город'],
                vacancy_percentage=row['Доля вакансий в %']
            )


def import_salary_area_backend():
    csv_file_path = os.path.join(project_root, 'salary_area_backend.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            SalaryAreaBackend.objects.create(
                area_name=row['Город'],
                average_salary=row['Уровень зарплат по городам']
            )


def import_dolya_area_backend():
    csv_file_path = os.path.join(project_root, 'dolya_area_backend.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            DolyaAreaBackend.objects.create(
                area_name=row['Город'],
                vacancy_percentage=row['Доля вакансий в %']
            )


def run():
    import_salary_area()
    import_dolya_area()
    import_salary_area_backend()
    import_dolya_area_backend()

