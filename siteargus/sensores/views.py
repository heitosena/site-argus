# Importa as funções para renderizar páginas e redirecionar
from django.shortcuts import render, redirect, get_object_or_404

# Importa HttpResponse para as páginas que ainda são estáticas
from django.http import HttpResponse

# Importa os modelos do aplicativo sensores
from .models import Dispositivo, Registro, LeituraSalva

# Importa mensagens do Django
from django.contrib import messages

# Garante que determinadas views aceitem somente POST
from django.views.decorators.http import require_POST


# Exibe a lista de dispositivos cadastrados
def lista_sensores(request):

    # Busca somente os dispositivos do usuário de teste
    dispositivos = Dispositivo.objects.filter(usuario_id=1)

    return render(
        request,
        "sensores/lista_sensores.html",
        {"dispositivos": dispositivos}
    )


# Exibe e processa o cadastro de um novo dispositivo
def cadastrar_sensor(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')
        modelo = request.POST.get('modelo')
        status = request.POST.get('status')

        # Verifica se a caixa de rede conectada foi marcada
        rede_conectada = request.POST.get('rede_conectada') == 'on'

        # Cria o dispositivo com bateria inicial de 100%
        # O valor poderá ser atualizado futuramente pelo ESP32.
        Dispositivo.objects.create(
            nome=nome,
            modelo=modelo,
            status=status,
            rede_conectada=rede_conectada,
            usuario_id=1
        )

        messages.success(
            request,
            f'O dispositivo "{nome}" foi cadastrado com sucesso!'
        )

        return redirect('cadastrar_sensor')

    return render(
        request,
        'sensores/cadastrar_sensor.html'
    )


# Exclui um dispositivo específico
@require_POST
def excluir_sensor(request, dispositivo_id):

    # Busca somente o dispositivo pertencente ao usuário de teste
    dispositivo = get_object_or_404(
        Dispositivo,
        id=dispositivo_id,
        usuario_id=1
    )

    nome = dispositivo.nome

    # Exclui somente o dispositivo selecionado.
    # O CASCADE também exclui sua localização e suas leituras originais.
    dispositivo.delete()

    messages.success(
        request,
        f'O dispositivo "{nome}" foi excluído com sucesso!'
    )

    return redirect('lista_sensores')


# Exibe as leituras dos dispositivos
def lista_leituras(request):

    registros = Registro.objects.select_related(
        'dispositivo'
    ).order_by('-data_hora')

    ultima_leitura = registros.first()

    return render(
        request,
        'sensores/lista_leituras.html',
        {
            'registros': registros,
            'ultima_leitura': ultima_leitura
        }
    )


# Salva cópias independentes das leituras selecionadas
def salvar_leituras(request):

    if request.method == 'POST':

        ids = request.POST.getlist('registros')

        registros = Registro.objects.filter(
            id__in=ids
        ).select_related('dispositivo')

        for registro in registros:

            LeituraSalva.objects.get_or_create(
                data_hora=registro.data_hora,
                dispositivo_nome=registro.dispositivo.nome,
                defaults={
                    'temperatura': registro.temperatura,
                    'umidade': registro.umidade,
                    'gas_percentual': registro.gas_percentual,
                    'nivel_gas': registro.nivel_gas,
                    'vazamento': registro.vazamento,
                }
            )

            registro.salvo = True
            registro.save(update_fields=['salvo'])

    return redirect('lista_leituras')


# Exclui somente as leituras originais
def excluir_leituras(request):

    if request.method == 'POST':

        ids = request.POST.getlist('registros')

        Registro.objects.filter(id__in=ids).delete()

    return redirect('lista_leituras')


# Exibe as cópias independentes das leituras salvas
def ver_leituras_salvas(request):

    registros = LeituraSalva.objects.all()

    ultima_leitura = registros.first()

    return render(
        request,
        'sensores/lista_leituras.html',
        {
            'registros': registros,
            'ultima_leitura': ultima_leitura,
            'mostrando_salvas': True,
        }
    )


# Exibe a página principal da Dashboard do A.R.G.U.S.
def dashboard(request):

    ultima_leitura = Registro.objects.select_related(
        'dispositivo'
    ).order_by('-data_hora').first()

    context = {
        'ultima_leitura': ultima_leitura,
    }

    return render(
        request,
        "dashboard.html",
        context
    )