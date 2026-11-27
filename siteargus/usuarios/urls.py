
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_views, name="login"),
    path("cadastro/", views.cadastro_views, name="cadastro"),
    path("dashboard/", views.dashboard_views, name="dashboard"),
    path("logout/", views.logout_views, name="logout"),

    path("telegram/conectar/", views.conectar_telegram_views, name="conectar_telegram"),
    path("telegram/receber/", views.receber_telegram_views, name="receber_telegram"),
]
