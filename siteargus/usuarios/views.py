from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_views(request):
    return render(request, "usuarios/login.html")

def cadastro_views(request):
    return HttpResponse("Pagina de cadastro")

def logout_views(request):
    return HttpResponse("Pagina de logout")

def dashboard_views(request):
    return HttpResponse("Pagina de Dashboard")