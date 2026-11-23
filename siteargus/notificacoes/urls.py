
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_contatos, name='listar_contatos'),
    path('adicionar/', views.adicionar_contato, name='adicionar_contato'),
    path('editar/<int:contato_id>/', views.editar_contato, name='editar_contato'),
    path('excluir/<int:contato_id>/', views.excluir_contato, name='excluir_contato'),
]
