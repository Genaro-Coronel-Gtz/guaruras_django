from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import (
    FormView, RedirectView, UpdateView, ListView,
    DetailView
    )
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core import signing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from braces.views import GroupRequiredMixin
from servicios.models import Servicio, SeguridadServicio, SeguridadJefeHijo
from .forms import LoginForm, UserRegisterForm, UserUpdateForm
from .models import Perfil, Ubicacion, Mensaje
from .filter import MensajeFilter

class LoginView(FormView):
    """!
    Clase que gestiona la vista principal del logeo de usuario

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 01-03-2017
    """
    form_class = LoginForm
    template_name = 'user.login.html'
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        """!
        Metodo que valida si el formulario es valido
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        usuario = form.cleaned_data['usuario']
        contrasena = form.cleaned_data['contrasena']
        usuario = authenticate(username=usuario, password=contrasena)
        if usuario.is_superuser or User.objects.filter(pk=usuario.id, groups__name='Administrador').exists():
            login(self.request, usuario)
            perfil = Perfil.objects.get(user=usuario)
            perfil.is_online=True
            perfil.save()
            if self.request.POST.get('remember_me') is not None:
                # Session expira a los dos meses si no se deslogea
                self.request.session.set_expiry(1209600)
        return super(LoginView, self).form_valid(form)
    
    
class LogoutView(RedirectView):
    """!
    Clase que gestiona la vista principal del deslogeo de usuario

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 01-03-2017
    """
    permanent = False
    query_string = True

    def get_redirect_url(self):
        """!
        Metodo que permite definir la url de dirección al ser válido el formulario
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna la url
        """
        perfil = Perfil.objects.get(user=self.request.user)
        logout(self.request)
        perfil.is_online=False
        perfil.onesignal_id=""
        perfil.save()
        return reverse_lazy('login')


class RegisterView(SuccessMessageMixin,GroupRequiredMixin, LoginRequiredMixin ,FormView):
    """!
    Muestra el formulario de registro de usuarios

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 09-01-2017
    """
    template_name = "user.register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('inicio')
    success_message = "Se registró con éxito"
    group_required = u"Administrador"
    model = User

    def form_valid(self, form, **kwargs):
        """!
        Metodo que valida si el formulario es valido

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 13-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """
        self.object = form.save()
        self.object.username = form.cleaned_data['username']
        self.object.set_password(form.cleaned_data['password1'])
        self.object.email = form.cleaned_data['email']
        self.object.save()

        self.object.groups.add(form.cleaned_data['group'])              

        perfil = Perfil()
        perfil.nombre_empresa = form.cleaned_data['nombre_empresa']
        perfil.user = self.object
        perfil.save() 

        # Si es cliente o jefe
        if(form.cleaned_data['group'].id!=1):
            servicio = Servicio()
            servicio.kilometraje = form.cleaned_data['kilometraje']
            servicio.velocidad = form.cleaned_data['velocidad']
            servicio.telefono = form.cleaned_data['telefono']
            servicio.frecuencia_rastreo = form.cleaned_data['frecuencia_rastreo']
            servicio.latitud_inicial = form.cleaned_data['latitud_inicial']
            servicio.longitud_inicial = form.cleaned_data['longitud_inicial']
            servicio.cliente = perfil
            servicio.save()

            # Si es cliente
            if(form.cleaned_data['group'].id==2):
                # Se asigna el jefe de seguridad
                perfil_jefe = form.cleaned_data['guardias']
                seguridad_servicio = SeguridadServicio()
                seguridad_servicio.servicio = servicio
                seguridad_servicio.guardia = perfil_jefe
                seguridad_servicio.save()

                # Se coloca como hijo al usuario
                seguridad_hijo = SeguridadJefeHijo()
                seguridad_hijo.pariente = perfil
                seguridad_hijo.jefe_seguridad = perfil_jefe
                seguridad_hijo.notificacion = form.cleaned_data['notificacion']
                seguridad_hijo.save()

        return super(RegisterView, self).form_valid(form)


class RegisterUpdate(SuccessMessageMixin,GroupRequiredMixin, LoginRequiredMixin, FormView):
    """!
    Muestra el formulario de actualizacion de usuarios

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-11-2017
    """
    template_name = "user.update.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy('user_list')
    success_message = "Se actualizó con éxito"
    group_required = u"Administrador"
    model = User

    def form_valid(self, form, **kwargs):
        """!
        Metodo que valida si el formulario es valido

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 15-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param form <b>{object}</b> Objeto que contiene el formulario de registro
        @return Retorna el formulario validado
        """ 
        user = User.objects.get(pk=self.kwargs['pk'])
        user.email = form.cleaned_data['email']
        user.save()    

        perfil = Perfil.objects.get(user_id=self.kwargs['pk'])
        perfil.nombre_empresa = form.cleaned_data['nombre_empresa']
        perfil.save() 

        return super(RegisterUpdate, self).form_valid(form)


    def get_initial(self):
        """!
        Metodo para agregar valores de inicio al formulario
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 15-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna los valores iniciales
        """
        initial = super(RegisterUpdate, self).get_initial()
        perfil = Perfil.objects.get(user_id=self.kwargs['pk'])
        initial['username'] = perfil.user.username
        initial['email'] = perfil.user.email
        initial['nombre_empresa'] = perfil.nombre_empresa
    
        return initial


class UserList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """!
    Muestra el listado de usuarios registrados

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 14-10-2017
    """
    template_name = "user.list.html"
    group_required = u"Administrador"
    model = Perfil
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 16-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['object_list'] = Perfil.objects.exclude(user__groups=1).order_by('user__date_joined').all()
        ## Implementación del paginador
        paginator = Paginator(kwargs['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
        return super(UserList, self).get_context_data(**kwargs)


class PerfilDetail(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    """!
    Muestra el detalle de usuarios

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-10-2017
    """
    template_name = "user.detail.html"
    group_required = u"Administrador"
    model = Perfil

    def post(self, *args, **kwargs):
        """!
        Metodo para manejar la petición del usuario
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 15-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna un redirect al usuario
        """
        perfil = Perfil.objects.get(pk=kwargs['pk'])
        user = perfil.user
        user.is_active = not user.is_active
        user.save()
        hab = "Habilitó" if user.is_active == True else "Deshabilitó"
        messages.success(self.request,'Se %s el usuario con éxito' % hab)
        return redirect(reverse_lazy('user_list'))


class UbicacionList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """!
    Clase que gestiona el listado de ubicaciones de un usuario en particular

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-10-2017
    """
    template_name = "ubicacion.list.html"
    group_required = u"Administrador"
    model = Ubicacion
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 16-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """

        kwargs['object_list'] = Ubicacion.objects.filter(usuario_id=int(self.kwargs['pk'])).order_by('fecha').all()
        ## Implementación del paginador
        paginator = Paginator(kwargs['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
        return super(UbicacionList, self).get_context_data(**kwargs)


class JefesList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """!
    Muestra el listado de jefes de seguridad

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 24-10-2017
    """
    template_name = "jefes.list.html"
    group_required = u"Administrador"
    model = Perfil
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 24-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['object_list'] = Perfil.objects.filter(user__groups__name='Jefe de Seguridad').order_by('user__date_joined').all()
        ## Implementación del paginador
        paginator = Paginator(kwargs['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
        return super(JefesList, self).get_context_data(**kwargs)

class MensajesDetail(GroupRequiredMixin, DetailView):
    template_name = "mensajes.detail.html"
    group_required = u"Administrador"
    model = Mensaje

class MensajesList(GroupRequiredMixin, ListView):
    """!
    Muestra el listado de mensajes enviados

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 12-11-2017
    """
    template_name = "mensajes.list.html"
    group_required = u"Administrador"
    model = Mensaje
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv2
        @date 12-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """

        kwargs['object_list'] = Mensaje.objects.filter().order_by('fecha').all()

        ## Filtrado
        kwargs['filter'] = MensajeFilter(self.request.GET, queryset=kwargs['object_list'])
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
        return super(MensajesList, self).get_context_data(**kwargs)