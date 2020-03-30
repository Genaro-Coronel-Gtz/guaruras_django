import django_filters.rest_framework
from rest_framework import generics, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from utils.one_signal_sdk import OneSignalSdk
from .serializers import AlertaSerializer
from .permissions import HasUserAlertasPermission
from alertas.models import Alerta
from base.constant import ONE_SIGNAL, TIPO_ALERTAS
from base.functions import get_jefe_user
from usuarios.models import Perfil
from servicios.models import Servicio

class AlertaViewSet(viewsets.ModelViewSet):
    """!
    Vista rest para el manejo de alertas

    @author Pablo Gónzalez (pdonaire1 at gmail)
    @date 15-10-2017
    """
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        """!
        Metodo para obtener el listado de alertas

        @author Pablo Gónzalez (pdonaire1 at gmail)
        @date 15-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna las alertas del usuario
        """
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).first()
        return Alerta.objects.filter(usuario=perfil)

    def perform_create(self, serializer):
        """!
        Metodo para realizar el guardado de alertas

        @author Pablo Gónzalez (pdonaire1 at gmail)
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 15-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param serializer <b>{object}</b> Serializador del modelo
        @return Retorna las alertas del usuario
        """
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).first()
        servicio = Servicio.objects.filter(cliente_id=perfil.pk).first()
        jefe_pariente = get_jefe_user(servicio.id,perfil)
        
        datos = serializer.save(usuario=perfil,servicio=servicio)
        
        tipo_alerta = dict(TIPO_ALERTAS)
        
        texto = "El usuario "+str(user.username)
        texto += " creó una nueva alerta de tipo " + str(tipo_alerta[serializer.data['tipo']]) + "\n"
        texto += " en " + serializer.data['ubicacion']
        
        data  = {'data':{'latitud':serializer.data['latitud'],'longitud':serializer.data['longitud'],
        'ubicacion':serializer.data['ubicacion'],'usuario':perfil.user.username,'tipo_alerta':str(tipo_alerta[serializer.data['tipo']])}}
        
        one_signal =  OneSignalSdk(ONE_SIGNAL['app_rest_id'], ONE_SIGNAL['app_id'])
        
        #Notificacion a dispositivos
        one_signal.create_notification(
            contents=texto,
            heading="Alerta",
            player_ids=jefe_pariente,
            kwargs=data,
            included_segments=(),
            )
        
        # Notificacion a Navegador
        one_signal.create_notification(
            contents=texto,
            heading="Alerta",
            url="http://guaruras.herokuapp.com/alertas/detalle/"+str(datos.id),
            included_segments=('Browser',),
            )