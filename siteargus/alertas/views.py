from django.shortcuts import render
from django.http import HttpResponse

def lista_alertas(request):
    return HttpResponse("Lista de alertas")
