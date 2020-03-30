from django.conf.urls import url
from .views import *

urlpatterns = [
    #url(r'^register$', ServicioRegister.as_view(), name = "servicio_register"),
    url(r'^list$', ServicioList.as_view(), name = "servicio_list"),
    url(r'^update/(?P<pk>\d+)$', ServicioUpdate.as_view(), name = "servicio_update"),
    url(r'^guardias-list/(?P<id>\d+)$', GuardiasList.as_view(), name = "guardias_list"),
    url(r'^jefes/list/(?P<id>\d+)$', JefesChildList.as_view(), name = "guardias_asignados_list"),
    url(r'^jefes/asignar/(?P<id>\d+)$', JefesChildRegister.as_view(), name = "jefe_guardia_asignar"),
    url(r'^jefes/pariente/delete/(?P<pk>\d+)/(?P<hijo>\d+)$', ParienteDelete.as_view(), name = "pariente_delete"),
    url(r'^jefes/pariente/update/(?P<pk>\d+)/(?P<hijo>\d+)$', ParienteUpdate.as_view(), name = "pariente_update"),
]
