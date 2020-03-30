from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from braces.views import GroupRequiredMixin
from base.functions import get_seguridad_servicios
from usuarios.models import Perfil
from .models import Servicio, SeguridadServicio, SeguridadJefeHijo
from .forms import ServicioForm, AsignarGuardiaFormset, AsignarGuardiaForm, ServicioUpdateForm

class ServicioRegister(SuccessMessageMixin, GroupRequiredMixin, LoginRequiredMixin, CreateView):
	"""!
	Clase que gestiona la creación de servicios

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 13-10-2017
	"""
	template_name = "servicio.create.html"
	form_class = ServicioForm
	success_url = reverse_lazy('inicio')
	success_message = "Se creó el registro con éxito"
	group_required = u"Administrador"
	model = Servicio

	def form_valid(self, form):
		"""!
		Metodo que valida si el formulario es valido

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 15-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param form <b>{object}</b> Objeto que contiene el formulario de registro
		@return Retorna el formulario validado
		"""
		self.object = form.save(commit=False)
		self.object.kilometraje = form.cleaned_data['kilometraje']
		self.object.velocidad = form.cleaned_data['velocidad']
		self.object.telefono = form.cleaned_data['telefono']
		self.object.frecuencia_rastreo = form.cleaned_data['frecuencia_rastreo']
		self.object.cliente = form.cleaned_data['cliente']
		self.object.save()

		# Si seleccionó guardias para el servicio
		if('guardias' in self.request.POST):
			post_data = dict(self.request.POST.lists())
			for item in post_data['guardias']:
				perfil = Perfil.objects.get(pk=int(item))
				seguridad_servicio = SeguridadServicio()
				seguridad_servicio.servicio = self.object
				seguridad_servicio.guardia = perfil
				seguridad_servicio.save()

		return super(ServicioRegister, self).form_valid(form)

class ServicioList(GroupRequiredMixin, LoginRequiredMixin, ListView):
	"""!
	Muestra el listado de servicios creados

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 14-10-2017
	"""
	template_name = "servicio.list.html"
	group_required = u"Administrador"
	model = Servicio
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
		kwargs['object_list'] = Servicio.objects.order_by('id').all()
		## Implementación del paginador
		paginator = Paginator(kwargs['object_list'], self.paginate_by)
		page = self.request.GET.get('page')
		try:
			kwargs['page_obj'] = paginator.page(page)
		except PageNotAnInteger:
			kwargs['page_obj'] = paginator.page(1)
		except EmptyPage:
			kwargs['page_obj'] = paginator.page(paginator.num_pages)
		return super(ServicioList, self).get_context_data(**kwargs)


class GuardiasList(GroupRequiredMixin, LoginRequiredMixin, ListView):
	"""!
	Muestra el listado de servicios creados

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 15-10-2017
	"""
	template_name = "guardias.list.html"
	group_required = u"Administrador"
	model = SeguridadServicio
	paginate_by = 10

	def get_context_data(self,**kwargs):
		"""!
		Metodo que obtiene el contexto de la vista

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 15-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param kwargs <b>{object}</b> Objeto que los argumentos clave de la vista
		@return Retorna el contexto de la vista
		"""
		kwargs['object_list'] = SeguridadServicio.objects.filter(servicio_id=int(self.kwargs['id'])).order_by('guardia__user__date_joined').all()
		## Implementación del paginador
		paginator = Paginator(kwargs['object_list'], self.paginate_by)
		page = self.request.GET.get('page')
		try:
			kwargs['page_obj'] = paginator.page(page)
		except PageNotAnInteger:
			kwargs['page_obj'] = paginator.page(1)
		except EmptyPage:
			kwargs['page_obj'] = paginator.page(paginator.num_pages)
		return super(GuardiasList, self).get_context_data(**kwargs)


class ServicioUpdate(SuccessMessageMixin, GroupRequiredMixin, LoginRequiredMixin, UpdateView):
	"""!
	Clase que gestiona la actualización de servicios

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 16-10-2017
	"""
	template_name = "servicio.update.html"
	form_class = ServicioUpdateForm
	success_url = reverse_lazy('servicio_list')
	success_message = "Se actualizó el registro con éxito"
	group_required = u"Administrador"
	model = Servicio

	def form_valid(self, form):
		"""!
		Metodo que valida si el formulario es valido

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 15-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param form <b>{object}</b> Objeto que contiene el formulario de registro
		@return Retorna el formulario validado
		"""
		self.object = form.save(commit=False)
		self.object.kilometraje = form.cleaned_data['kilometraje']
		self.object.velocidad = form.cleaned_data['velocidad']
		self.object.latitud_inicial = form.cleaned_data['latitud_inicial']
		self.object.longitud_inicial = form.cleaned_data['longitud_inicial']
		self.object.telefono = form.cleaned_data['telefono']
		self.object.frecuencia_rastreo = form.cleaned_data['frecuencia_rastreo']
		self.object.save()

		# Si seleccionó guardias para el servicio
		guardia = form.cleaned_data['guardias']
		seguridad_servicios = SeguridadServicio.objects.filter(servicio_id=int(self.kwargs['pk'])).first()
		if(guardia.id!=seguridad_servicios.guardia.id):
			seguridad_servicios.guardia = guardia
			seguridad_servicios.save()

		return super(ServicioUpdate, self).form_valid(form)

	def get_initial(self):
		"""!
		Metodo para agregar valores de inicio al formulario

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 13-11-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@return Retorna los valores iniciales
		"""
		initial = super(ServicioUpdate, self).get_initial()
		try:
			seguridad_servicios = SeguridadServicio.objects.filter(servicio_id=int(self.kwargs['pk'])).first()
			initial['guardias'] = seguridad_servicios.guardia_id
		except:
			pass

		return initial


class JefesChildList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    """!
    Muestra el listado de guardias asignados a un jefe de seguridad

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 24-10-2017
    """
    template_name = "jefes.child.list.html"
    group_required = u"Administrador"
    model = SeguridadJefeHijo
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
        id_seguridad = int(self.kwargs['id'])
        kwargs['id'] = id_seguridad
        kwargs['object_list'] = SeguridadJefeHijo.objects.filter(jefe_seguridad_id=id_seguridad).order_by('jefe_seguridad_id').all()
        ## Implementación del paginador
        paginator = Paginator(kwargs['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        try:
            kwargs['page_obj'] = paginator.page(page)
        except PageNotAnInteger:
            kwargs['page_obj'] = paginator.page(1)
        except EmptyPage:
            kwargs['page_obj'] = paginator.page(paginator.num_pages)
        return super(JefesChildList, self).get_context_data(**kwargs)


class JefesChildRegister(GroupRequiredMixin, LoginRequiredMixin, CreateView):
	"""!
	Muestra el listado de guardias asignados a un jefe de seguridad

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 24-10-2017
	"""
	template_name = "jefes.child.create.html"
	group_required = u"Administrador"
	model = SeguridadJefeHijo
	form_class = AsignarGuardiaFormset
	success_message = "Se asignó el pariente con éxito"
	success_url = reverse_lazy("jefes_list")

	def form_valid(self, form):
		"""!
		Metodo que valida si el formulario es valido

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 24-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param form <b>{object}</b> Objeto que contiene el formulario de registro
		@return Retorna el formulario validado
		"""
		jefe = Perfil.objects.get(pk=int(self.kwargs['id']))

		form_set = AsignarGuardiaFormset(self.request.POST,instance=jefe)
		if(form_set.is_valid()):
			form_set.save()
		messages.success(self.request,self.success_message)
		return redirect(self.success_url)

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
		kwargs['id'] = self.kwargs['id']
		return super(JefesChildRegister, self).get_context_data(**kwargs)

class ParienteDelete(SuccessMessageMixin,GroupRequiredMixin, LoginRequiredMixin, DeleteView):
	"""!
	Clase que gestiona el borrado de la asignación de parientes

	@author Rodrigo Boet (rboet at cenditel.gob.ve)
	@date 31-10-2017
	"""
	model = SeguridadJefeHijo
	template_name = "pariente.delete.html"
	success_message = "Se eliminó el pariente con éxito"
	success_url = reverse_lazy('jefes_list')
	group_required = u"Administrador"

	def get_object(self, **kwargs):
		"""!
		Metodo que permite cargar el objeto

		@author Rodrigo Boet (rboet at cenditel.gob.ve)
		@copyright GNU/GPLv2
		@date 31-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
		@return Retorna los datos de contexto
		"""
		return SeguridadJefeHijo.objects.filter(pariente_id=int(self.kwargs['hijo']),jefe_seguridad_id=int(self.kwargs['pk'])).get()

class ParienteUpdate(SuccessMessageMixin,GroupRequiredMixin, LoginRequiredMixin, UpdateView):
	"""!
	Clase que gestiona el actualizado de la asignación de parientes

	@author Rodrigo Boet (rboet at cenditel.gob.ve)
	@date 13-11-2017
	"""
	model = SeguridadJefeHijo
	form_class = AsignarGuardiaForm
	template_name = "jefes.child.update.html"
	success_message = "Se actualizó el pariente con éxito"
	success_url = reverse_lazy('jefes_list')
	group_required = u"Administrador"

	def get_object(self, **kwargs):
		"""!
		Metodo que permite cargar el objeto
	
		@author Rodrigo Boet (rboet at cenditel.gob.ve)
		@copyright GNU/GPLv2
		@date 13-11-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
		@return Retorna los datos de contexto
		"""
		return SeguridadJefeHijo.objects.filter(pariente_id=int(self.kwargs['hijo']),jefe_seguridad_id=int(self.kwargs['pk'])).get()


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
		kwargs['pk'] = self.kwargs['pk']
		return super(ParienteUpdate, self).get_context_data(**kwargs)