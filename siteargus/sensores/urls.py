from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_sensores, name='lista_sensores'),
    path('cadastrar/', views.cadastrar_sensor, name='cadastrar_sensor'),
    path('leituras/', views.lista_leituras, name='lista_leituras'),
]