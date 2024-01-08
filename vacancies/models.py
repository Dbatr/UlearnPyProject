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

