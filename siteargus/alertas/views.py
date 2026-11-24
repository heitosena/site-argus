from django.shortcuts import render, redirect
from .models import Alerta


# Exibe os cinco alertas mais recentes do usuário conectado
def lista_alertas(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    alertas = Alerta.objects.filter(
        dispositivo__usuario_id=usuario_id
    ).select_related(
        'dispositivo'
    ).order_by('-data_criacao')[:5]

    return render(
        request,
        'alertas/lista_alertas.html',
        {'alertas': alertas}
    )