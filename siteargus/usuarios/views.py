
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

from .models import Usuario


def login_views(request):
    return render(request, "usuarios/login.html")


def cadastro_views(request):

    if request.method == "POST":

        # Recebendo os dados do formulário
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip().lower()
        telefone = re.sub(r"\D", "", request.POST.get("telefone", ""))
        senha = request.POST.get("senha", "")
        confSenha = request.POST.get("confSenha", "")

        # Validando o nome
        if len(nome) < 7:
            return render(request, "usuarios/cadastro.html", {
                "erro": "Digite seu nome completo."
            })

        # Validando o e-mail
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "usuarios/cadastro.html", {
                "erro": "Digite um e-mail válido."
            })

        # Validando a senha
        if len(senha) < 8:
            return render(request, "usuarios/cadastro.html", {
                "erro": "A senha deve ter no mínimo 8 caracteres."
            })

        if senha != confSenha:
            return render(request, "usuarios/cadastro.html", {
                "erro": "As senhas não coincidem."
            })

        # Validando o telefone
        if len(telefone) not in (10, 11):
            return render(request, "usuarios/cadastro.html", {
                "erro": "Digite um telefone válido."
            })

        # Verificando se o e-mail já existe
        if Usuario.objects.filter(email=email).exists():
            return render(request, "usuarios/cadastro.html", {
                "erro": "Este e-mail já está cadastrado."
            })

        # Criptografando a senha
        senhaHash = make_password(senha)

        # Salvando os dados no MySQL
        Usuario.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senhaHash
        )

        return redirect("login")

    return render(request, "usuarios/cadastro.html")


def logout_views(request):
    return render(request, "usuarios/logout.html")


def dashboard_views(request):
    return render(request, "usuarios/dashboard.html")


def cadastrodisp_views(request):
    return render(request, "usuarios/cadastrodisp.html")
