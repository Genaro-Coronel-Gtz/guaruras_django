from rest_framework import serializers
from servicios.models import Servicio

class ServicioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servicio
        fields = ('id', 'kilometraje', 'velocidad', 'telefono', 'frecuencia_rastreo', 'cliente', 'latitud_inicial', 'longitud_inicial')
