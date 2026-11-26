from django.urls import path, include
from . import views 

urlpatterns = [
    path('receber/', views.receber_dados, name='receber_dados'),
    path('dashboard/', views.consultar_dashboard, name='consultar_dashboard'),
]