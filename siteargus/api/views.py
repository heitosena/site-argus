
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from sensores.models import Dispositivo, Registro   
from .serializers import RegistroSerializer



@api_view(['POST'])
def receber_dados(request):

    mac_address = request.data.get('mac_address')

    # Verifica se o MAC Address foi informado
    if not mac_address or not isinstance(mac_address, str):
        return Response(
            {'erro': 'MAC Address não informado ou inválido.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Padroniza o MAC Address
    mac_address = mac_address.strip().upper()

    # Procura o dispositivo ou cria um provisório
    dispositivo, criado = Dispositivo.objects.get_or_create(
        mac_address=mac_address,
        defaults={
            'nome': 'ESP32 - Aguardando cadastro',
            'usuario_id': None,
            'status': 'Ativo',
            'rede_conectada': True,
            'ultima_comunicacao': timezone.now()
        }
    )

    # Atualiza a comunicação
    dispositivo.ultima_comunicacao = timezone.now()
    dispositivo.rede_conectada = True
    dispositivo.save(
        update_fields=[
            'ultima_comunicacao',
            'rede_conectada'
        ]
    )

    # Se o POST contém somente o MAC, registra a detecção
    campos_leitura = [
        'temperatura',
        'umidade',
        'gas_percentual',
        'nivel_gas',
        'vazamento'
    ]

    if not any(campo in request.data for campo in campos_leitura):
        return Response(
            {
                'mensagem': 'Dispositivo detectado com sucesso!',
                'dispositivo_id': dispositivo.id,
                'mac_address': dispositivo.mac_address,
                'cadastrado': dispositivo.usuario_id is not None
            },
            status=status.HTTP_201_CREATED
        )

    # Valida os dados da leitura
    serializer = RegistroSerializer(data=request.data)

    if serializer.is_valid():

        registro = serializer.save(dispositivo=dispositivo)

        return Response(
            {
                'mensagem': 'Leitura registrada com sucesso!',
                'registro_id': registro.id,
                'dispositivo_id': dispositivo.id,
                'mac_address': dispositivo.mac_address
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            'erro': 'Dados inválidos.',
            'detalhes': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def consultar_dashboard(request):

    usuario_id = request.session.get('usuario_id')

    if usuario_id is None:
        return Response(
            {'erro': 'Usuário não autenticado.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    dispositivos = Dispositivo.objects.filter(usuario_id=usuario_id)

    registros = Registro.objects.filter(
        dispositivo__usuario_id=usuario_id
    ).order_by('-data_hora')

    ultima_leitura = registros.first()

    historico_gas = registros.order_by('data_hora').values(
        'data_hora',
        'gas_percentual'
    )[:20]

    return Response({
        'total_dispositivos': dispositivos.count(),
        'dispositivos_ativos': dispositivos.filter(status='Ativo').count(),
        'dispositivos_inativos': dispositivos.filter(status='Inativo').count(),
        'dispositivos_manutencao': dispositivos.filter(status='Manutenção').count(),

        'ultima_leitura': {
            'temperatura': float(ultima_leitura.temperatura),
            'umidade': float(ultima_leitura.umidade),
            'gas_percentual': ultima_leitura.gas_percentual,
            'nivel_gas': ultima_leitura.nivel_gas,
            'vazamento': ultima_leitura.vazamento,
        } if ultima_leitura else None,

        'historico_gas': [
            {
                'data_hora': registro['data_hora'],
                'gas_percentual': registro['gas_percentual']
            }
            for registro in historico_gas
        ]
    })
