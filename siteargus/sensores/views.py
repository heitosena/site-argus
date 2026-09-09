from django.shortcuts import render
from django.http import HttpResponse

#importa o modelo Dispositivo do aplicativo sensores 
from .models import Dispositivo 


# Cria a função reponsavel pela pagina de lista de sensores 
def lista_sensores(request):
    #Busca todos os dispositivos cadastrados no banco de dados 
    dispositivos = Dispositivo.objects.all() 

    return render (
        request,
        "sensores/lista_sensores.html",
        {"dispositivos": dispositivos}
    )


# Exibe a tela para cadastrar um novo sensor
def cadastrar_sensor(request):
    return HttpResponse("Cadastro de sensor")


# Exibe as leituras dos sensores
def lista_leituras(request):
    return HttpResponse("Lista de leituras")