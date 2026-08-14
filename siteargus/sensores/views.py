from django.shortcuts import render
from django.http import HttpResponse


# Exibe a lista de sensores cadastrados
def lista_sensores(request):
    return HttpResponse("Lista de sensores")


# Exibe a tela para cadastrar um novo sensor
def cadastrar_sensor(request):
    return HttpResponse("Cadastro de sensor")


# Exibe as leituras dos sensores
def lista_leituras(request):
    return HttpResponse("Lista de leituras")