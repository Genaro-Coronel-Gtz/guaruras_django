from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, FormView, DetailView
from braces.views import GroupRequiredMixin
from utils.one_signal_sdk import OneSignalSdk
from .models import Alerta
from .forms import SendNotificationForm
from .filter import AlertaFilter
from base.constant import ONE_SIGNAL, TIPO_ALERTAS

class AlertasList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """!
    Muestra el listado de alertas de un usuario en específico

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 14-10-2017
    """
    template_name = "alerta.list.html"
    group_required = u"Administrador"
    model = Alerta
    paginate_by = 10

    def get_context_data(self,**kwargs):
        """!
        Metodo que obtiene el contexto de la vista

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 14-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que los argumentos clave de la vista
        @return Retorna el contexto de la vista
        """
        if('id' in self.kwargs):
            kwargs['object_list'] = Alerta.objects.filter(usuario_id=int(self.kwargs['id'])).order_by('-fecha').all()
        else:
            kwargs['object_list'] = Alerta.objects.order_by('-fecha').all()

        # Filtrado
        kwargs['filter'] = AlertaFilter(self.request.GET, queryset=kwargs['object_list'])
        kwargs['object_list'] = kwargs['filter'].qs

        ## Implementación del paginador
        paginator = Paginator(kwargs['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)

        kwargs['tipo_alerta'] = dict(TIPO_ALERTAS)

        return super(AlertasList, self).get_context_data(**kwargs)

class AlertasNotification(SuccessMessageMixin,GroupRequiredMixin, LoginRequiredMixin, FormView):
    """!
    Envía notificaciones de una alerta a los guardias seleccionados

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 18-10-2017
    """
    template_name = "alerta.notification.html"
    form_class = SendNotificationForm
    group_required = u"Administrador"
    success_message = "Se enviaron las notificaciones con éxito"
    success_url = reverse_lazy("alerta_all_list")

    def form_valid(self, form, **kwargs):
        """!
        Metodo que valida si el formulario es valido

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 18-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        guardias_list = form.cleaned_data['guardias_list']
        alerta = Alerta.objects.get(id=int(self.kwargs['id']))
        tipo_alerta = dict(TIPO_ALERTAS)
        texto = "Se presentó una alerta de tipo "+tipo_alerta[alerta.tipo]
        texto += " en la fecha "+alerta.fecha.strftime("%d-%m-%Y %H:%M:%S")+"\n"
        texto += ".En las coordenadas lat: "+alerta.latitud+" y long: "+alerta.longitud

        one_signal =  OneSignalSdk(ONE_SIGNAL['app_rest_id'], ONE_SIGNAL['app_id'])
        guardias_os_list = []
        for guardia in guardias_list:
            if guardia.onesignal_id!=None or guardia.onesignal_id!='':
                guardias_os_list.append(guardia.onesignal_id)
        data  = {'data':{'latitud':alerta.latitud,'longitud':alerta.longitud,
        'ubicacion':alerta.ubicacion,'usuario':alerta.usuario.user.username,'tipo_alerta':tipo_alerta[alerta.tipo]}}
        create_notification(
            contents=texto,
            heading="Alerta",
            player_ids=guardias_os_list,
            url="http://guaruras.herokuapp.com/alertas/",
            kwargs=data,
            included_segments=(),
            )

        return super(AlertasNotification, self).form_valid(form)


class AlertasDetail(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    """!
    Muestra el detalle de la alerta

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 26-11-2017
    """
    template_name = "alerta.detail.html"
    group_required = u"Administrador"
    model = Alerta

    def get_context_data(self,**kwargs):
        """!
        Metodo que obtiene el contexto de la vista

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 26-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que los argumentos clave de la vista
        @return Retorna el contexto de la vista
        """
        kwargs['tipo_alerta'] = dict(TIPO_ALERTAS)

        return super(AlertasDetail, self).get_context_data(**kwargs)