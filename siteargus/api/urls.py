from django.urls import path, include
from . import views 

urlpatterns = [
    path('receber/', views.receber_dados, name='receber_dados'),
]