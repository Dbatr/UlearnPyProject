from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index),
    path('demand/', views.demand),
    path('geography/', views.geography),
]