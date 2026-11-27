
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import re
import secrets
import json

from .models import Usuario


def login_views(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        senha = request.POST.get("senha", "")

        usuario = Usuario.objects.filter(email=email).first()

        if usuario and check_password(senha, usuario.senha):
            request.session["usuario_id"] = usuario.id
            request.session["usuario_nome"] = usuario.nome
            return redirect("dashboard")

        return render(
            request,
            "usuarios/login.html",
            {"erro": "E-mail ou senha incorretos."}
        )

    return render(request, "usuarios/login.html")


def cadastro_views(request):
    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip().lower()
        telefone = re.sub(r"\D", "", request.POST.get("telefone", ""))
        senha = request.POST.get("senha", "")
        confSenha = request.POST.get("confSenha", "")

        if len(nome) < 7:
            return render(
                request,
                "usuarios/cadastro.html",
                {"erro": "Digite seu nome completo."}
            )

        try:
            validate_email(email)
        except ValidationError:
            return render(
                request,
                "usuarios/cadastro.html",
                {"erro": "Digite um e-mail válido."}
            )

        if len(senha) < 8:
            return render(
                request,
                "usuarios/cadastro.html",
                {"erro": "A senha deve ter no mínimo 8 caracteres."}
            )

        if senha != confSenha:
            return render(
                request,
                "usuarios/cadastro.html",
                {"erro": "As senhas não coincidem."}
            )

        if len(telefone) not in (10, 11):
            return render(
                request,
                "usuarios/cadastro.html",
                {"erro": "Digite um telefone válido."}
            )

        if Usuario.objects.filter(email=email).exists():
            return render(
                request,
                "usuarios/cadastro.html",
                {"erro": "Este e-mail já está cadastrado."}
            )

        senhaHash = make_password(senha)

        Usuario.objects.create(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senhaHash
        )

        return redirect("login")

    return render(request, "usuarios/cadastro.html")


def logout_views(request):
    request.session.flush()
    return redirect("login")


def dashboard_views(request):
    return render(request, "usuarios/dashboard.html")


def cadastrodisp_views(request):
    return render(request, "usuarios/cadastrodisp.html")


def conectar_telegram_views(request):
    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("login")

    usuario = Usuario.objects.filter(id=usuario_id).first()

    if not usuario:
        return redirect("login")

    codigo = secrets.token_urlsafe(24)

    usuario.telegram_link_code = codigo
    usuario.save(update_fields=["telegram_link_code"])

    link = f"https://t.me/ARGUS_Alertas_Bot?start={codigo}"

    return redirect(link)


@csrf_exempt
def receber_telegram_views(request):
    if request.method != "POST":
        return JsonResponse(
            {"erro": "Método não permitido"},
            status=405
        )

    try:
        dados = json.loads(request.body)

        mensagem = dados.get("message", {})
        texto = mensagem.get("text", "")
        chat_id = mensagem.get("chat", {}).get("id")

        if not texto.startswith("/start ") or not chat_id:
            return JsonResponse(
                {"erro": "Mensagem inválida"},
                status=400
            )

        codigo = texto.split(" ", 1)[1].strip()

        usuario = Usuario.objects.filter(
            telegram_link_code=codigo
        ).first()

        if not usuario:
            return JsonResponse(
                {"erro": "Código inválido"},
                status=404
            )

        usuario.telegram_chat_id = str(chat_id)
        usuario.telegram_link_code = None

        usuario.save(update_fields=[
            "telegram_chat_id",
            "telegram_link_code"
        ])

        return JsonResponse({"sucesso": True})

    except (ValueError, TypeError, KeyError):
        return JsonResponse(
            {"erro": "Dados inválidos"},
            status=400
        )
