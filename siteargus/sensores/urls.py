from django.urls import path
from . import views


# URLS relacionadas ao app de sensores
urlpatterns = [
    # Lista de sensores cadastrados
    path('', views.lista_sensores, name='lista_sensores'),

    # Tela para cadastrar um sensor
    path('cadastrar/', views.cadastrar_sensor, name='cadastrar_sensor'),

    # Lista as leituras dos sensores
    path('leituras/', views.lista_leituras, name='lista_leituras'),
]