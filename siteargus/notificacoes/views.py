from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

from .models import ContatoNotificacao


# Exibe os contatos adicionais do usuário conectado.
def listar_contatos(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    contatos = ContatoNotificacao.objects.filter(
        usuario_id=usuario_id
    ).order_by('-data_criacao')

    return render(
        request,
        'notificacoes/notificacoes.html',
        {
            'contatos': contatos
        }
    )


# Cadastra um novo contato para o usuário conectado.
@require_POST
def adicionar_contato(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    tipo = request.POST.get("tipo", "").strip()
    valor = request.POST.get("valor", "").strip()

    if tipo not in ['email', 'telefone']:
        messages.error(request, "Tipo de contato inválido.")
        return redirect('configuracoes')

    if not valor:
        messages.error(request, "Informe o contato.")
        return redirect('configuracoes')

    if tipo == 'email':

        valor = valor.lower()

        try:
            validate_email(valor)
        except ValidationError:
            messages.error(request, "Digite um e-mail válido.")
            return redirect('configuracoes')

    elif tipo == 'telefone':

        valor = re.sub(r'\D', '', valor)

        if len(valor) not in (10, 11):
            messages.error(request, "Digite um telefone válido.")
            return redirect('configuracoes')

    # Impede cadastrar o mesmo contato duas vezes na mesma conta.
    if ContatoNotificacao.objects.filter(
        usuario_id=usuario_id,
        tipo=tipo,
        valor=valor
    ).exists():

        messages.error(request, "Este contato já está cadastrado.")
        return redirect('configuracoes')

    ContatoNotificacao.objects.create(
        usuario_id=usuario_id,
        tipo=tipo,
        valor=valor
    )

    messages.success(request, "Contato cadastrado com sucesso.")

    return redirect('configuracoes')


# Edita um contato pertencente ao usuário conectado.
@require_POST
def editar_contato(request, contato_id):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    contato = get_object_or_404(
        ContatoNotificacao,
        id=contato_id,
        usuario_id=usuario_id
    )

    tipo = request.POST.get("tipo", "").strip()
    valor = request.POST.get("valor", "").strip()

    if tipo not in ['email', 'telefone'] or not valor:
        messages.error(request, "Preencha os dados corretamente.")
        return redirect('configuracoes')

    if tipo == 'email':

        valor = valor.lower()

        try:
            validate_email(valor)
        except ValidationError:
            messages.error(request, "Digite um e-mail válido.")
            return redirect('configuracoes')

    elif tipo == 'telefone':

        valor = re.sub(r'\D', '', valor)

        if len(valor) not in (10, 11):
            messages.error(request, "Digite um telefone válido.")
            return redirect('configuracoes')

    duplicado = ContatoNotificacao.objects.filter(
        usuario_id=usuario_id,
        tipo=tipo,
        valor=valor
    ).exclude(id=contato_id).exists()

    if duplicado:
        messages.error(request, "Este contato já está cadastrado.")
        return redirect('configuracoes')

    contato.tipo = tipo
    contato.valor = valor
    contato.save()

    messages.success(request, "Contato atualizado com sucesso.")

    return redirect('configuracoes')


# Exclui um contato pertencente ao usuário conectado.
@require_POST
def excluir_contato(request, contato_id):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    contato = get_object_or_404(
        ContatoNotificacao,
        id=contato_id,
        usuario_id=usuario_id
    )

    contato.delete()

    messages.success(request, "Contato excluído com sucesso.")

    return redirect('configuracoes')
