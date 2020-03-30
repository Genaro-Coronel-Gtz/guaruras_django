import django_filters.rest_framework
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from utils.one_signal_sdk import OneSignalSdk
from base.constant import ONE_SIGNAL
from servicios.models import SeguridadJefeHijo
from usuarios.serializers import UbicacionSerializer, PerfilSerialzer
from usuarios.models import Ubicacion, Perfil, Mensaje
from .permissions import HasUserUbicacionPermission
from .serializers import UbicacionSerializer, PerfilSerialzer, MensajeSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    # model = Ubicacion
    serializer_class = UbicacionSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = [AllowAny, ]
    http_method_names = ['get','head','post', 'options']

    def get_queryset(self):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).all()
        return Ubicacion.objects.filter(usuario=perfil)

    def perform_create(self, serializer):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).get()
        serializer.save(usuario=perfil)

    @list_route(methods=['get'], permission_classes=[])
    def hijos_ubicacion(self, request):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).get()
        try:
            hijos_ids = SeguridadJefeHijo.objects.filter(jefe_seguridad=perfil)\
                .values_list('pariente_id', flat=True)
            ubicaciones = Ubicacion.objects.filter(
                usuario_id__in=hijos_ids
            ).order_by('usuario','-fecha').distinct('usuario__id')
            return Response(UbicacionSerializer(ubicaciones, many=True).data)
        except: return Response({})

    @list_route(methods=['get'], permission_classes=[])
    def mis_hijos(self, request):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).get()
        hijos_ids = SeguridadJefeHijo.objects.filter(jefe_seguridad=perfil)\
            .values_list('pariente_id', flat=True)
        hijos = Perfil.objects.filter(id__in=hijos_ids)
        return Response(PerfilSerialzer(hijos, many=True).data)

    @list_route(methods=['get'], permission_classes=[])
    def hijos_ubicaciones(self, request):
        """
        Recibe por parametros hijo_perfil_id, inicio, fin, puede ser none
        """
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).get()
        inicio = self.request.GET.get("inicio", None)
        fin = self.request.GET.get("fin", None)
        hijo_perfil_id = self.request.GET.get("hijo_perfil_id", None)
        # try:
        hijos = SeguridadJefeHijo.objects.filter(jefe_seguridad=perfil)
        hijos_ids = hijos.values_list('pariente_id', flat=True)
        ubicaciones = Ubicacion.objects.filter(
            usuario_id__in=hijos_ids
        ).order_by('-fecha')
        if inicio:
            ubicaciones = ubicaciones.filter(fecha__gte=inicio)
        if fin:
            ubicaciones = ubicaciones.filter(fecha__lte=fin)
        if hijo_perfil_id:
            ubicaciones = ubicaciones.filter(usuario_id=hijo_perfil_id)
        if not inicio or not fin:
            ubicaciones = ubicaciones[:100]
        return Response(UbicacionSerializer(ubicaciones, many=True).data)
        # except: return Response({})

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
        # user = self.request.user
        # perfil = Perfil.objects.filter(user=user).first()
        # user = User.objects.get(id=perfil.user.id)
        # if not user.is_admin:
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # try:
        #     instance = self.get_object()
        #     self.perform_destroy(instance)
        # except Http404:
        #     pass
        # return Response(status=status.HTTP_204_NO_CONTENT)


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    # model = Ubicacion
    serializer_class = PerfilSerialzer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # permission_classes = (IsAuthenticated,)
    permission_classes = [AllowAny, ]
    http_method_names = ['get','head','put']

    def get_queryset(self):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        # user = self.request.user
        perfil = Perfil.objects.filter(user=user).all()
        return perfil

    # @list_route(methods=['put'], permission_classes=[])
    # def telefono(self, request, pk=None):
    #     if 'telefono' in request.data:
    #         token = Token.objects.get(key=self.request.GET['token'])
    #         user = token.user
    #         # user = self.request.user.id
    #         perfil = Perfil.objects.get(user_id=user)
    #         perfil.telefono = request.data['telefono']
    #         perfil.save()
    #         return Response("Se actualizó el telefono con éxito", status=status.HTTP_201_CREATED)
    #     return Response("Debeenviar el telefono", status=status.HTTP_400_BAD_REQUEST)

class MensajeViewSet(viewsets.ModelViewSet):
    """!
    Vista rest para el manejo de mensajes

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 12-11-2017
    """
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = [AllowAny, ]
    http_method_names = ['get','head','post', 'options']

    def get_queryset(self):
        """!
        Metodo para obtener el listado de mensajes

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 12-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna las mensajes del usuario
        """
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).all()
        return Mensaje.objects.filter(usuario=perfil)

    def perform_create(self, serializer):
        """!
        Metodo para crear un mensaje

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 12-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param serializer <b>{object}</b> Objeto serializador del modelo
        """
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).get()
        
        mensaje = serializer.save(usuario=perfil)
        
        one_signal =  OneSignalSdk(ONE_SIGNAL['app_rest_id'], ONE_SIGNAL['app_id'])
        one_signal.create_notification(
            contents="Tiene un nuevo mensaje",
            heading="Nuevo Mensaje",
            included_segments=('Browser',),
            url="http://guaruras.herokuapp.com/mensajes/{}".format(mensaje.id),
            )