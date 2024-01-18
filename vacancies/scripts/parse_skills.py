# python manage.py runscript parse_skills -v2
import csv
from collections import Counter


def save_skills_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year', 'Skill', 'Count'])
        for year, skills_count in data.items():
            for skill, count in skills_count.items():
                writer.writerow([year, skill, count])


def run():
    skills_all_by_year = {}
    skills_backend_by_year = {}

    with open('vacancies.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            year = row['published_at'][:4]
            skills = row['key_skills'].split('\n')

            # Очистка и разделение навыков
            skills = [skill.strip() for skill in skills if skill.strip()]

            # Проверка наличия года в словаре, инициализация списка при необходимости
            if year in skills_all_by_year:
                skills_all_by_year[year].extend(skills)
            else:
                skills_all_by_year[year] = skills

            # Проверка наличия ключевых навыков в имени вакансии
            backend_keywords = ['Backend-программист', 'backend', 'бэкэнд', 'бэкенд', 'бекенд', 'бекэнд', 'back end',
                                'бэк энд', 'бэк енд', 'django', 'flask', 'laravel', 'yii', 'symfony']
            if any(word in row['name'].lower() for word in backend_keywords):
                if year in skills_backend_by_year:
                    skills_backend_by_year[year].extend(skills)
                else:
                    skills_backend_by_year[year] = skills

    for data, filename in zip([skills_all_by_year, skills_backend_by_year],
                              ['all_skills.csv', 'backend_skills.csv']):
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Year', 'Skill', 'Count'])
            for year, skills in data.items():
                skills_count = Counter(skills)
                for skill, count in skills_count.most_common(20):
                    writer.writerow([year, skill, count])

    print("Done")

