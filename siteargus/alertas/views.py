from django.shortcuts import render
from django.http import HttpResponse

# Exibe a lista de alertas registrados
def lista_alertas(request):
    return HttpResponse("Lista de alertas")
