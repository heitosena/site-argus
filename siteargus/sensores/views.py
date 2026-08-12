from django.shortcuts import render
from django.http import HttpResponse

def lista_sensores(request):
    return HttpResponse("Lista de sensores")

def cadastrar_sensor(request):
    return HttpResponse("Cadastro de sensor")

def lista_leituras(request):
    return HttpResponse("Lista de leituras")