from django.urls import path
from . import views

urlpatterns = [
    # Lista de sensores cadastrados.
    path('', views.lista_sensores, name='lista_sensores'),

    # Tela para cadastrar um sensor.
    path('cadastrar/', views.cadastrar_sensor, name='cadastrar_sensor'),

    # Exclui um dispositivo específico.
    path(
        'excluir-dispositivo/<int:dispositivo_id>/',
        views.excluir_sensor,
        name='excluir_sensor'
    ),

    # Tela de Dashboard.
    path('dashboard/', views.dashboard, name='dashboard'),

    # Lista as leituras dos sensores.
    path('leituras/', views.lista_leituras, name='lista_leituras'),

    # Salva as leituras selecionadas pelo usuário.
    path('salvar-leituras/', views.salvar_leituras, name='salvar_leituras'),

    # Exclui as leituras selecionadas pelo usuário.
    path(
        'excluir-leituras/',
        views.excluir_leituras,
        name='excluir_leituras'
    ),

    # Exibe as leituras salvas.
    path(
        'leituras-salvas/',
        views.ver_leituras_salvas,
        name='ver_leituras_salvas'
    ),
]