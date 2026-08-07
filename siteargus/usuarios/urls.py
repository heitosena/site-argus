from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_views, name="login"),
    path("cadastro/", views.cadastro_views, name="cadastro"),
    path("dashboard/", views.dashboard_views, name="dashboard"),
    path ("logout/", views.logout_views, name="logout")
]