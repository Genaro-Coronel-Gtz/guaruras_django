from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views
from .views import obtain_user_auth_token, logout_user_auth_token, AdministratorPhone
from .router import router
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('base.urls')),
    url(r'^', include('usuarios.urls')),
    url(r'^servicios/', include('servicios.urls')),
    url(r'^alertas/', include('alertas.urls')),
    url(r'^api/v1/api-token-auth/', obtain_user_auth_token),
    url(r'^api/v1/api-token-logout/', logout_user_auth_token),
    url(r'^api/v1/get-admin-phone/', AdministratorPhone.as_view()),
    url(r'^api/v1/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
