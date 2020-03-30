from django.conf.urls import url, include
from .views import (
    Inicio, 
    TerminosCondicionesFormView, 
    TerminosCondicionesView, 
    TerminosCondicionesAPIView
)
from utils.views import ResetPasswordViewSet, ChangePasswordViewSet

urlpatterns = [
    url(r'^$', Inicio.as_view(), name = "inicio"),
    url(r'^terminos-update/$', TerminosCondicionesFormView.as_view(), name = "update-terminos"),
    url(r'^terminos/$', TerminosCondicionesView.as_view(), name = "terminos"),
    url(r'^api/v1/terminos-api/$', TerminosCondicionesAPIView.as_view(), name = "terminos-api"),
    url(r'^api/v1/reset-password/', ResetPasswordViewSet.as_view()),
    url(r'^api/v1/change-password/', ChangePasswordViewSet.as_view()),
    
]