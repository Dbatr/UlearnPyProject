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
