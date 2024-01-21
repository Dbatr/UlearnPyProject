from django.db import models

# Create your models here.


class Vacancy(models.Model):
    name = models.TextField(null=True, default=None)
    key_skills = models.TextField(null=True, default=None)
    salary_from = models.IntegerField(null=True, default=None)
    salary_to = models.IntegerField(null=True, default=None)
    salary_currency = models.CharField(max_length=10, null=True, default=None)
    area_name = models.TextField(null=True, default=None)
    published_at = models.DateTimeField(null=False, default=None)

    def __str__(self):
        return f"{self.name} {self.area_name} {self.published_at}"

    class Meta:
        db_table = 'vacancies'
        indexes = [
            models.Index(fields=['name'], name='name_idx')
        ]
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    pass


class Currency(models.Model):
    date = models.CharField(max_length=7)  # Например, "YYYY-MM"
    byr = models.FloatField(null=True, blank=True)
    usd = models.FloatField(null=True, blank=True)
    eur = models.FloatField(null=True, blank=True)
    kzt = models.FloatField(null=True, blank=True)
    uah = models.FloatField(null=True, blank=True)
    azn = models.FloatField(null=True, blank=True)
    kgs = models.FloatField(null=True, blank=True)
    uzs = models.FloatField(null=True, blank=True)
    gel = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.date}"

    class Meta:
        ordering = ['date']
        db_table = 'currency'  # Имя таблицы в базе данных

        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"


class ProcessedVacancy(models.Model):
    name = models.TextField(null=True, default=None)
    salary = models.IntegerField(null=True, default=None)
    area_name = models.TextField(null=True, default=None)
    published_at = models.DateTimeField(null=False, default=None)

    def __str__(self):
        return f"{self.name} {self.area_name} {self.published_at}"

    class Meta:
        db_table = 'processed_vacancies'
        verbose_name = "Обработанная вакансия"
        verbose_name_plural = "Обработанные вакансии"


class VacancyStats(models.Model):
    year = models.CharField(max_length=4)
    vacancy_count = models.IntegerField()

    def __str__(self):
        return f"{self.year} - {self.vacancy_count} вакансий"

    class Meta:
        db_table = 'vacancy_stats'
        verbose_name = "Статистика по количеству вакансий"
        verbose_name_plural = "Статистика по количеству вакансий"


class AvgSalaryStats(models.Model):
    year = models.CharField(max_length=4)
    average_salary = models.FloatField()

    def __str__(self):
        return f"{self.year} - Средняя зарплата: {self.average_salary}"

    class Meta:
        db_table = 'avg_salary_stats'
        verbose_name = "Статистика по средней зарплате"
        verbose_name_plural = "Статистика по средней зарплате"


class BackendStats(models.Model):
    year = models.CharField(max_length=4)
    backend_vacancy_count = models.IntegerField()

    def __str__(self):
        return f"{self.year} - Вакансий для бэкенд-программистов: {self.backend_vacancy_count}"

    class Meta:
        db_table = 'backend_stats'
        verbose_name = "Статистика по Backend-программистам"
        verbose_name_plural = "Статистика по Backend-программистам"


class BackendAvgSalaryStats(models.Model):
    year = models.CharField(max_length=4)
    backend_average_salary = models.FloatField()

    def __str__(self):
        return f"{self.year} - Средняя зарплата для бэкенд-программистов: {self.backend_average_salary}"

    class Meta:
        db_table = 'backend_avg_salary_stats'
        verbose_name = "Статистика по средней зарплате Backend-программистов"
        verbose_name_plural = "Статистика по средней зарплате Backend-программистов"


class SalaryArea(models.Model):
    area_name = models.CharField(max_length=255)
    average_salary = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.average_salary}"

    class Meta:
        db_table = 'salary_area'
        verbose_name = "Уровень зарплат по городам"
        verbose_name_plural = "Уровень зарплат по городам"


class DolyaArea(models.Model):
    area_name = models.CharField(max_length=255)
    vacancy_percentage = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.vacancy_percentage}"

    class Meta:
        db_table = 'dolya_area'
        verbose_name = "Доля вакансий по городам"
        verbose_name_plural = "Доля вакансий по городам"


class SalaryAreaBackend(models.Model):
    area_name = models.CharField(max_length=255)
    average_salary = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.average_salary}"

    class Meta:
        db_table = 'salary_area_backend'
        verbose_name = "Уровень зарплат по городам для бэкендера"
        verbose_name_plural = "Уровень зарплат по городам для бэкендера"


class DolyaAreaBackend(models.Model):
    area_name = models.CharField(max_length=255)
    vacancy_percentage = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.vacancy_percentage}"

    class Meta:
        db_table = 'dolya_area_backend'
        verbose_name = "Доля вакансий по городам для бэкендера"
        verbose_name_plural = "Доля вакансий по городам для бэкендера"
