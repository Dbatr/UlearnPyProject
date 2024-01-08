from django.contrib import admin
from .models import Vacancy, Currency, ProcessedVacancy

# Register your models here.

admin.site.register(Vacancy)
admin.site.register(Currency)
admin.site.register(ProcessedVacancy)
