from rest_framework import serializers
from alertas.models import Alerta

class AlertaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alerta
        fields = ('id', 'tipo', 'latitud', 'longitud', 'atendida', 'fecha','ubicacion')

    def create(self, validated_data):
        """!
        Método para generar el modelo a partir del serializer

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 26-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param validated_data <b>{object}</b> Objeto que contiene la data validada
        @return Retorna el objeto de Alerta
        """
        return Alerta.objects.create(**validated_data)
