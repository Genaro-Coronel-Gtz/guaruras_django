from rest_framework.decorators import detail_route, list_route
from servicios.models import Servicio
from rest_framework import viewsets
from .serializers import ServicioSerializer
from rest_framework import generics
import django_filters.rest_framework
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from usuarios.models import Perfil
from rest_framework.authtoken.models import Token
from .permissions import HasUserServicioPermission

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = [AllowAny]
    http_method_names = ['get','head']

    def get_queryset(self):
        token = Token.objects.get(key=self.request.GET['token'])
        user = token.user
        perfil = Perfil.objects.filter(user=user).first()
        return Servicio.objects.filter(cliente=perfil)

    def perform_create(self, serializer):
        user = self.request.user
        perfil = Perfil.objects.filter(user=user).first()
        serializer.save(cliente=perfil)

