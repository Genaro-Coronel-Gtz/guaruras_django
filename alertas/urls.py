from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^$', AlertasList.as_view(), name = "alerta_all_list"),
    url(r'^(?P<id>\d+)$', AlertasList.as_view(), name = "alerta_list"),
    url(r'^detalle/(?P<pk>\d+)$', AlertasDetail.as_view(), name = "alerta_detail"),
    url(r'^notification/(?P<id>.+)$', AlertasNotification.as_view(), name = "send_notification"),
]