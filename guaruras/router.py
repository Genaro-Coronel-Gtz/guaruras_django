from rest_framework import routers
from usuarios.api_v1_views import UbicacionViewSet, PerfilViewSet, MensajeViewSet
from alertas.api_v1_views import AlertaViewSet
from servicios.api_v1_views import ServicioViewSet

router = routers.SimpleRouter()
router.register(r'ubicacion', UbicacionViewSet)
router.register(r'alertas', AlertaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'perfil', PerfilViewSet)
router.register(r'mensajes', MensajeViewSet)
