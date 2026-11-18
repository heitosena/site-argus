from django.shortcuts import render
from .models import Alerta


# Exibe os cinco alertas mais recentes
def lista_alertas(request):

    alertas = Alerta.objects.select_related(
        'dispositivo'
    ).order_by('-data_criacao')[:5]

    return render(
        request,
        'alertas/lista_alertas.html',
        {'alertas': alertas}
    )