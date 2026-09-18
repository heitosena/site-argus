# Importa as funções para renderizar páginas e redirecionar
from django.shortcuts import render, redirect

# Importa HttpResponse para as páginas que ainda são estáticas
from django.http import HttpResponse

# Importa o modelo Dispositivo do aplicativo sensores
from .models import Dispositivo


# Exibe a lista de sensores cadastrados
def lista_sensores(request):
    # Busca todos os dispositivos cadastrados no banco de dados
    dispositivos = Dispositivo.objects.all()

    # Envia os dispositivos para o template HTML
    return render(
        request,
        "sensores/lista_sensores.html",
        {"dispositivos": dispositivos}
    )


# Exibe e processa o cadastro de um novo sensor
def cadastrar_sensor(request):
    # Verifica se o formulário foi enviado
    if request.method == 'POST':

        # Pega os dados enviados pelo formulário
        nome = request.POST.get('nome')
        modelo = request.POST.get('modelo')
        status = request.POST.get('status')
        bateria = request.POST.get('bateria')

        # Verifica se a caixa de rede conectada foi marcada
        rede_conectada = request.POST.get('rede_conectada') == 'on'

        # Cria o dispositivo no banco de dados
        Dispositivo.objects.create(
            nome=nome,
            modelo=modelo,
            status=status,
            bateria=bateria,
            rede_conectada=rede_conectada
        )

        # Volta para a lista depois de salvar
        return redirect('lista_sensores')

    # Mostra o formulário quando a página é aberta
    return render(
        request,
        'sensores/cadastrar_sensor.html'
    )


# Exibe as leituras dos sensores
def lista_leituras(request):
    return HttpResponse("Lista de leituras")