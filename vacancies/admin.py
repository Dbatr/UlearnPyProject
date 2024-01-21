from django.contrib import admin
from .models import *


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_name', 'published_at')
    fields = ('name', 'key_skills', ('salary_from', 'salary_to', 'salary_currency'), 'area_name', 'published_at')
    search_fields = ['name', 'area_name']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('date', 'byr', 'usd', 'eur', 'kzt', 'uah', 'azn', 'kgs', 'uzs', 'gel')
    search_fields = ['date']


class ProcessedVacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'salary', 'area_name', 'published_at')
    search_fields = ['name', 'area_name']
    list_filter = ['published_at']


# Регистрация моделей
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ProcessedVacancy, ProcessedVacancyAdmin)

admin.site.register(VacancyStats)
admin.site.register(AvgSalaryStats)
admin.site.register(BackendStats)
admin.site.register(BackendAvgSalaryStats)

admin.site.register(SalaryArea)
admin.site.register(DolyaArea)
admin.site.register(SalaryAreaBackend)
admin.site.register(DolyaAreaBackend)

