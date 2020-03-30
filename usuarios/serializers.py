from rest_framework import serializers
from usuarios.models import Ubicacion, Perfil, Mensaje

class UbicacionSerializer(serializers.ModelSerializer):
    usuario_full_name = serializers.SerializerMethodField()
    class Meta:
        model = Ubicacion
        fields = ('id', 'latitud', 'longitud', 'fecha', 'usuario_id', 'usuario_full_name', 'formatted_address')
    
    def get_usuario_full_name(self, obj):
        return obj.usuario.user.username + ' ' + obj.usuario.user.first_name + ' ' + obj.usuario.user.last_name 

# class PerfilSerialzer(serializers.ModelSerializer):
#     """
#     Clase Serializadora del modelo Perfil

#     @author Rodrigo Boet (rudmanmrrod at gmail)
#     @date 16-10-17
#     """

#     class Meta:
#         model = Perfil
#         exclude = ('telefono',)


class PerfilSerialzer(serializers.ModelSerializer):
    """
    Clase Serializadora del modelo Perfil

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 16-10-17
    """
    usuario_full_name = serializers.SerializerMethodField()
    class Meta:
        model = Perfil
        # fields = '__all__'
        fields = ('id', 'nombre_empresa', 'onesignal_id', 'user', 'is_online', 'usuario_full_name')

    def get_usuario_full_name(self, obj):
        return obj.user.username + ' ' + obj.user.first_name + ' ' + obj.user.last_name 


class MensajeSerializer(serializers.ModelSerializer):
    """
    Clase Serializadora del modelo Mensaje

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 12-11-17
    """

    class Meta:
        model = Mensaje
        fields = ('id', 'mensaje', 'usuario_id','fecha')

    def create(self, validated_data):
        """!
        Método para generar el modelo a partir del serializer

        @author Pablo Donaire (pdonaire1 at gmail)
        @date 27-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param validated_data <b>{object}</b> Objeto que contiene la data validada
        @return Retorna el objeto de Mensaje
        """
        return Mensaje.objects.create(**validated_data)
