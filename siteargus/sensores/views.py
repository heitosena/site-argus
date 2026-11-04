# Importa as funções para renderizar páginas e redirecionar
from django.shortcuts import render, redirect

# Importa HttpResponse para as páginas que ainda são estáticas
from django.http import HttpResponse

# Importa o modelo Dispositivo do aplicativo sensores
from .models import Dispositivo, Registro, LeituraSalva

from django.contrib import messages


# Exibe a lista de sensores cadastrados
def lista_sensores(request):
    # Busca somente os dispositivos do usuário de teste
    dispositivos = Dispositivo.objects.filter(usuario_id=1)

    # Envia os dispositivos para o template HTML
    return render(
        request,
        "sensores/lista_sensores.html",
        {"dispositivos": dispositivos}
    )


# Exibe e processa o cadastro de um novo dispositivo
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

        # Cria o dispositivo vinculado ao usuário de teste
        Dispositivo.objects.create(
            nome=nome,
            modelo=modelo,
            status=status,
            bateria=bateria,
            rede_conectada=rede_conectada,
            usuario_id=1
        )

        # Exibe a mensagem de sucesso
        messages.success(
            request,
            f'O dispositivo "{nome}" foi cadastrado com sucesso!'
        )

        # Volta para a tela de cadastro
        return redirect('cadastrar_sensor')

    # Mostra o formulário
    return render(
        request,
        'sensores/cadastrar_sensor.html'
    )

# Exibe as leituras dos dispositivos.
def lista_leituras(request):
    # Busca todas as leituras, da mais recente para a mais antiga.
    registros = Registro.objects.select_related('dispositivo').order_by('-data_hora')

    # Busca a leitura mais recente, caso exista alguma.
    ultima_leitura = registros.first()

    # Envia o histórico e a leitura mais recente para a página HTML.
    return render(
        request,
        'sensores/lista_leituras.html',
        {
            'registros': registros,
            'ultima_leitura': ultima_leitura
        }
       
)   
# Salva cópias independentes das leituras selecionadas.
def salvar_leituras(request):
    if request.method == 'POST':

        # Recebe os IDs selecionados pelo usuário.
        ids = request.POST.getlist('registros')

        # Busca as leituras originais.
        registros = Registro.objects.filter(
            id__in=ids
        ).select_related('dispositivo')

        # Cria uma cópia de cada leitura na tabela de salvas.
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

            # Mantém a marcação antiga por compatibilidade.
            registro.salvo = True
            registro.save(update_fields=['salvo'])

    return redirect('lista_leituras')


# Exclui somente as leituras originais.
def excluir_leituras(request):
    if request.method == 'POST':

        # Recebe os IDs selecionados.
        ids = request.POST.getlist('registros')

        # Exclui somente da tabela registros.
        Registro.objects.filter(id__in=ids).delete()

    return redirect('lista_leituras')


# Exibe as cópias independentes das leituras salvas.
def ver_leituras_salvas(request):

    # Consulta diretamente a tabela leituras_salvas.
    registros = LeituraSalva.objects.all()

    # Busca a leitura salva mais recente.
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
    # Busca a última leitura registrada.
    ultima_leitura = Registro.objects.select_related(
        'dispositivo'
    ).order_by('-data_hora').first()

    context = {
        'ultima_leitura': ultima_leitura,
    }

    # Abre o template HTML da Dashboard enviando os dados reais.
    return render(request, "dashboard.html", context)