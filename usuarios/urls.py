from django.conf.urls import url
from django.contrib.auth.views import *
from .forms import PasswordResetForm, PasswordConfirmForm
from .views import *
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^login$', LoginView.as_view(), name = "login"),
    url(r'^logout$', LogoutView.as_view(), name = "logout"),
    url(r'^register$', RegisterView.as_view(), name = "register"),
    url(r'^user/list$', UserList.as_view(), name = "user_list"),
    url(r'^user/update/(?P<pk>\d+)$', RegisterUpdate.as_view(), name = "user_update"),
    url(r'^user/(?P<pk>\d+)$', PerfilDetail.as_view(), name = "user_detail"),
    url(r'^user/ubicacion-list/(?P<pk>\d+)$', UbicacionList.as_view(), name = "ubicacion_list"),
    url(r'^jefes/list$', JefesList.as_view(), name = "jefes_list"),
    url(r'^mensajes/list$', MensajesList.as_view(), name = "mensajes_list"),
    url(r'^mensajes/(?P<pk>\d+)$$', MensajesDetail.as_view(), name = "mensajes_detail"),
    url(r'^password/reset/$', password_reset,
        {'post_reset_redirect': '/password/done/',
         'template_name': 'user.reset.html', 'password_reset_form':PasswordResetForm}, name="reset"),
    url(r'^password/done/$', password_reset_done,
        {'template_name': 'user.passwordreset.done.html'},
        name='reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'user.passwordreset.confirm.html', 'set_password_form':PasswordConfirmForm,
         'post_reset_redirect': '/password/end/'},
        name='password_reset_confirm'),
    url(r'^password/end/$', password_reset_done,
        {'template_name': 'user.passwordreset.end.html'},
        name='reset_end'),
    # url(r'^api/docs/', include_docs_urls(title='My API title', public=False))
]