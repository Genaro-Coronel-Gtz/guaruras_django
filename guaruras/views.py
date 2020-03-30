from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.models import Perfil
from servicios.models import Servicio, SeguridadServicio

class ObtainUserAuthToken(APIView):
    """!
    Vista génerica para obtener el token de sessión si el usuario es de tipo cliente

    @author Pablo Gónzalez (pdonaire1 at gmail)
    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-10-2017
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        if('password' in request.data and 'username'in request.data and 'onesignal_id' in request.data):
            user = serializer.validated_data['user']
            group_name = user.groups.first().name;
            if(group_name=='Cliente' or group_name=='Jefe de Seguridad'):
                token, created = Token.objects.get_or_create(user=user)
                onesignal_id = request.data['onesignal_id']
                perfil = Perfil.objects.filter(user= user).get()
                perfil.onesignal_id = onesignal_id
                perfil.is_online = True
                perfil.save()
                return Response({
                    'token': token.key, 
                    'perfil_id': perfil.id,
                    'username': perfil.user.username,
                    'group':group_name
                    })
            else:
                return Response("No tiene permisos para acceder aquí", status=status.HTTP_403_FORBIDDEN)    
        else:
            return Response("Debe enviar todos los párametros", status=status.HTTP_400_BAD_REQUEST)


class LogOutUserAuthToken(APIView):
    """!
    Vista génerica para obtener el token de sessión si el usuario es de tipo cliente

    @author Pablo Gónzalez (pdonaire1 at gmail)
    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-10-2017
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).get()
        perfil.is_online = False
        perfil.onesignal_id=""
        perfil.save()
        # token.delete() lo comentamos por si tiene dos telefonos

        return Response({'success': True}, status=status.HTTP_200_OK)

class AdministratorPhone(APIView):
    """!
    Vista génerica para obtener el telefono del administrador
    @author Pablo Gónzalez (pdonaire1 at gmail)
    @date 07-11-2017
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    # serializer_class = AuthTokenSerializer

    def get(self, request, *args, **kwargs):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        if (user.groups.first().name=="Cliente"):
            servicio = Servicio.objects.filter(cliente__user=user).first()
        else:
            servicio = SeguridadServicio.objects.filter(guardia__user=user).first().servicio
        return Response(
            {'success': True, 'telefono': servicio.telefono}, 
            status=status.HTTP_200_OK)



obtain_user_auth_token = ObtainUserAuthToken.as_view()
logout_user_auth_token = LogOutUserAuthToken.as_view()
