from django.urls import path
from . import views

# URLS relacionada ao app de alertas
urlpatterns = [
    # Lista os alertas registrados
    path('', views.lista_alertas, name='lista_alertas'),

]