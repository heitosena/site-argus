
# Importa as funções para renderizar páginas e redirecionar
from django.shortcuts import render, redirect, get_object_or_404

# Importa HttpResponse para as páginas que ainda são estáticas
from django.http import HttpResponse

# Importa os modelos do aplicativo sensores
from .models import Dispositivo, Registro, LeituraSalva

from usuarios.models import Usuario

# Importa mensagens do Django
from django.contrib import messages

# Garante que determinadas views aceitem somente POST
from django.views.decorators.http import require_POST

from notificacoes.models import ContatoNotificacao


# Exibe a lista de dispositivos cadastrados
def lista_sensores(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    # Busca somente os dispositivos do usuário conectado.
    dispositivos = Dispositivo.objects.filter(usuario_id=usuario_id)

    return render(
        request,
        "sensores/lista_sensores.html",
        {"dispositivos": dispositivos}
    )



# Exibe e processa o cadastro de um novo dispositivo

def cadastrar_sensor(request):
    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    if request.method == 'POST':
        dispositivo_id = request.POST.get('dispositivo_id')
        nome = request.POST.get('nome', '').strip()
        modelo = request.POST.get(
            'modelo',
            'ESP32 - Sensor de Gás'
        )
        status = request.POST.get('status')
        rede_conectada = request.POST.get('rede_conectada') == 'on'

        status_validos = ['Ativo', 'Inativo', 'Manutenção']

        if not dispositivo_id or not nome or status not in status_validos:
            messages.error(
                request,
                'Preencha os campos corretamente e selecione um dispositivo.',
                extra_tags='cadastro'
            )
            return redirect('cadastrar_sensor')

        quantidade = Dispositivo.objects.filter(
            id=dispositivo_id,
            usuario_id__isnull=True
        ).update(
            nome=nome,
            modelo=modelo,
            status=status,
            rede_conectada=rede_conectada,
            usuario_id=usuario_id
        )

        if quantidade == 0:
            messages.error(
                request,
                'Este dispositivo não está mais disponível. Atualize a página.',
                extra_tags='cadastro'
            )
            return redirect('cadastrar_sensor')

        messages.success(
            request,
            f'O dispositivo "{nome}" foi cadastrado com sucesso!',
            extra_tags='cadastro'
        )

        # Retorna para a lista após cadastrar com sucesso.
        return redirect('lista_sensores')

    dispositivos_disponiveis = Dispositivo.objects.filter(
        usuario_id__isnull=True
    ).order_by('-ultima_comunicacao')

    return render(
        request,
        'sensores/cadastrar_sensor.html',
        {
            'dispositivos_disponiveis': dispositivos_disponiveis
        }
    )


    

#exibe a tela de editar o dispositivo selecionado
def editar_sensor(request, dispositivo_id):
    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    dispositivo = get_object_or_404(
        Dispositivo,
        id=dispositivo_id,
        usuario_id=usuario_id
    )

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        status = request.POST.get('status', '')
        rede_conectada = request.POST.get('rede_conectada') == 'on'

        # Verifica se o nome foi preenchido.
        if not nome:
            messages.error(
                request,
                'Informe um nome para o dispositivo.',
                extra_tags='dispositivo'
            )
            return redirect('lista_sensores')

        # Verifica se o status enviado é válido.
        status_validos = ['Ativo', 'Inativo', 'Manutenção']

        if status not in status_validos:
            messages.error(
                request,
                'Selecione um status válido para o dispositivo.',
                extra_tags='dispositivo'
            )
            return redirect('lista_sensores')

        dispositivo.nome = nome
        dispositivo.status = status
        dispositivo.rede_conectada = rede_conectada

        dispositivo.save(
            update_fields=['nome', 'status', 'rede_conectada']
        )

        messages.success(
            request,
            f'O dispositivo "{nome}" foi atualizado com sucesso!',
            extra_tags='dispositivo'
        )

    return redirect('lista_sensores')



# Exclui um dispositivo específico
@require_POST
def excluir_sensor(request, dispositivo_id):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    # Busca somente o dispositivo pertencente ao usuário conectado.
    dispositivo = get_object_or_404(
        Dispositivo,
        id=dispositivo_id,
        usuario_id=usuario_id
    )

    nome = dispositivo.nome

    # Exclui somente o dispositivo selecionado.
    # O CASCADE também exclui sua localização e suas leituras originais.
    dispositivo.delete()

    messages.success(
        request,
        f'O dispositivo "{nome}" foi excluído com sucesso!',
        extra_tags='dispositivo'
    )

    return redirect('lista_sensores')


# Exibe as leituras dos dispositivos
def lista_leituras(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    registros = Registro.objects.filter(
        dispositivo__usuario_id=usuario_id
    ).select_related(
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
@require_POST
def salvar_leituras(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    ids = request.POST.getlist('registros')

    # Busca somente leituras do usuário que ainda não foram salvas.
    registros = Registro.objects.filter(
        id__in=ids,
        dispositivo__usuario_id=usuario_id,
        salvo=False
    ).select_related('dispositivo')

    for registro in registros:

        # Cria uma cópia independente da leitura vinculada ao usuário.
        LeituraSalva.objects.create(
            usuario_id=usuario_id,
            data_hora=registro.data_hora,
            dispositivo_nome=registro.dispositivo.nome,
            temperatura=registro.temperatura,
            umidade=registro.umidade,
            gas_percentual=registro.gas_percentual,
            nivel_gas=registro.nivel_gas,
            vazamento=registro.vazamento
        )

        # Marca o registro original como salvo.
        registro.salvo = True
        registro.save(update_fields=['salvo'])

    return redirect('lista_leituras')


# Exclui as leituras selecionadas pelo usuário.
@require_POST
def excluir_leituras(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    ids = request.POST.getlist('registros')

    # Identifica se a exclusão veio da tela de leituras salvas.
    origem_salvas = request.POST.get('origem_salvas') == '1'

    if not ids:
        messages.warning(
            request,
            'Selecione pelo menos uma leitura para excluir.',
            extra_tags='leitura'
        )

    else:

        # Exclui cópias independentes das leituras salvas.
        if origem_salvas:

            quantidade, _ = LeituraSalva.objects.filter(
                id__in=ids,
                usuario_id=usuario_id
            ).delete()

            if quantidade:
                messages.success(
                    request,
                    f'{quantidade} leitura(s) salva(s) excluída(s) com sucesso!',
                    extra_tags='leitura'
                )

        # Exclui somente as leituras originais do usuário.
        else:

            quantidade, _ = Registro.objects.filter(
                id__in=ids,
                dispositivo__usuario_id=usuario_id
            ).delete()

            if quantidade:
                messages.success(
                    request,
                    f'{quantidade} leitura(s) excluída(s) com sucesso!',
                    extra_tags='leitura'
                )

    # Retorna para a tela de onde a exclusão foi solicitada.
    if origem_salvas:
        return redirect('ver_leituras_salvas')

    return redirect('lista_leituras')


# Exibe as cópias independentes das leituras salvas
def ver_leituras_salvas(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    registros = LeituraSalva.objects.filter(
        usuario_id=usuario_id
    )

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

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    # Busca os dispositivos do usuário conectado.
    dispositivos = Dispositivo.objects.filter(usuario_id=usuario_id)

    # Calcula a quantidade de dispositivos cadastrados.
    total_dispositivos = dispositivos.count()

    # Calcula a quantidade de dispositivos ativos.
    dispositivos_ativos = dispositivos.filter(
        status='Ativo'
    ).count()

    # Calcula a quantidade de dispositivos inativos.
    dispositivos_inativos = dispositivos.filter(
        status='Inativo'
    ).count()

    # Calcula a quantidade de dispositivos em manutenção.
    dispositivos_manutencao = dispositivos.filter(
        status='Manutenção'
    ).count()

    # Busca a última leitura dos dispositivos do usuário.
    ultima_leitura = Registro.objects.filter(
        dispositivo__usuario_id=usuario_id
    ).select_related(
        'dispositivo'
    ).order_by('-data_hora').first()

    # Busca as últimas 20 leituras de gás.
    historico_gas = list(
        Registro.objects.filter(
            dispositivo__usuario_id=usuario_id
        ).order_by(
            '-data_hora'
        ).values(
            'data_hora',
            'gas_percentual'
        )[:20]
    )

    # Inverte a ordem para apresentar as leituras da mais antiga à mais recente.
    historico_gas.reverse()

    # Organiza as informações enviadas para o HTML.
    context = {
        'ultima_leitura': ultima_leitura,

        'total_dispositivos': total_dispositivos,
        'dispositivos_ativos': dispositivos_ativos,
        'dispositivos_inativos': dispositivos_inativos,
        'dispositivos_manutencao': dispositivos_manutencao,

        'historico_gas': historico_gas,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


# Exibe a página de configurações do A.R.G.U.S.
def configuracoes(request):

    usuario_id = request.session.get("usuario_id")

    if usuario_id is None:
        return redirect('login')

    # Busca os dados do usuário conectado.
    usuario = Usuario.objects.filter(id=usuario_id).first()

    if usuario is None:
        return redirect('login')

    # Busca os contatos adicionais do usuário.
    contatos = ContatoNotificacao.objects.filter(
        usuario_id=usuario_id
    )

    # Separa os e-mails e telefones.
    contatos_email = contatos.filter(tipo='email')

    contatos_telefone = contatos.filter(tipo='telefone')

    # Conta os contatos cadastrados.
    total_emails = contatos_email.count()

    total_telefones = contatos_telefone.count()

    return render(
        request,
        'configuracao/configuracoes.html',
        {
            'usuario': usuario,
            'contatos_email': contatos_email,
            'contatos_telefone': contatos_telefone,
            'total_emails': total_emails,
            'total_telefones': total_telefones
        }
    )