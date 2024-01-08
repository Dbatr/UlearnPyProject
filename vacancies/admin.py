from django.contrib import admin
from .models import Vacancy
from .models import Currency

# Register your models here.

admin.site.register(Vacancy)
admin.site.register(Currency)
