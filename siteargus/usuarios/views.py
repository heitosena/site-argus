from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

# Create your views here.
def login_views(request):
    return render(request, "usuarios/login.html")

# Método de armazenar as informações de cadastro de usuario (ainda sem conectar no MySQL)...
def cadastro_views(request):

    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        senha = request.POST.get("senha")

        senha = make_password(senha)

        print(nome)
        print(email)
        print(telefone)
        print(senha)

    return render(request, "usuarios/cadastro.html")

def logout_views(request):
    return render(request, "usuarios/logout.html")

def dashboard_views(request):
    return render(request, "usuarios/dashboard.html")

def cadastrodisp_views(request):
    return render(request, "usuarios/cadastrodisp.html")