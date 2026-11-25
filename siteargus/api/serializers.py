
from rest_framework import serializers
from sensores.models import Registro


class RegistroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registro

        fields = [
            'temperatura',
            'umidade',
            'gas_percentual',
            'nivel_gas',
            'vazamento',
        ]
