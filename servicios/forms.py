from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.models import User
from .models import Servicio, SeguridadJefeHijo
from usuarios.models import Perfil

class ServicioForm(ModelForm):
	"""!
	Clase del formulario de creación de servicios

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 01-03-2017
	"""

	def __init__(self, *args, **kwargs):
		"""!
		Metodo que sobreescribe cuando se inicializa el formulario

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 01-03-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param args <b>{list}</b> Lista de los argumentos
		@param kwargs <b>{dict}</b> Diccionario con argumentos
		@return Retorna el formulario validado
		"""
		super(ServicioForm, self).__init__(*args, **kwargs)
		self.fields['kilometraje'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Límite de Kilométraje'})
		self.fields['velocidad'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Límite de velocidad'})
		self.fields['velocidad'].required = False
		self.fields['telefono'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Télefono'})
		self.fields['frecuencia_rastreo'].widget = forms.Select()
		self.fields['frecuencia_rastreo'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Frecuencia de Rastreo (mínutos)'})
		self.fields['frecuencia_rastreo'].widget.choices=(('','Seleccione un valor...'),('5','5'),('10','10'),('15','15'),('30','30'))
		self.fields['cliente'].queryset = Perfil.objects.filter(user__groups=2).all()
		self.fields['cliente'].widget.attrs.update({'class': 'form-control'})
		self.fields['cliente'].empty_label = "Seleccione un cliente..."
		# Latitud y Longitud
		self.fields['latitud_inicial'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Latitud','readonly':True})
		self.fields['longitud_inicial'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Longitud','readonly':True})

	# Listado de guardias 
	guardias = forms.ModelChoiceField(
		widget=forms.Select(attrs={'class':'form-control'}),
		queryset = Perfil.objects.filter(user__groups=3).all(),
		label="Jefe de Seguridad", empty_label = "Seleccione un jefe de seguridad..."
		)

	class Meta:
		model = Servicio
		fields = '__all__'
		# exclude = ('velocidad',)

class ServicioUpdateForm(ModelForm):
	"""!
	Clase del formulario de actualización de servicios

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 15-11-2017
	"""

	def __init__(self, *args, **kwargs):
		"""!
		Metodo que sobreescribe cuando se inicializa el formulario

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 01-03-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param args <b>{list}</b> Lista de los argumentos
		@param kwargs <b>{dict}</b> Diccionario con argumentos
		@return Retorna el formulario validado
		"""
		super(ServicioUpdateForm, self).__init__(*args, **kwargs)
		self.fields['kilometraje'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Límite de Kilométraje'})
		self.fields['velocidad'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Límite de velocidad'})
		self.fields['velocidad'].required = False
		self.fields['telefono'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Télefono'})
		self.fields['frecuencia_rastreo'].widget = forms.Select()
		self.fields['frecuencia_rastreo'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Frecuencia de Rastreo (mínutos)'})
		self.fields['frecuencia_rastreo'].widget.choices=(('','Seleccione un valor...'),('5','5'),('10','10'),('15','15'),('30','30'))
		# Latitud y Longitud
		self.fields['latitud_inicial'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Latitud','readonly':True})
		self.fields['longitud_inicial'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Longitud','readonly':True})

	# Listado de guardias 
	guardias = forms.ModelChoiceField(
		widget=forms.Select(attrs={'class':'form-control'}),
		queryset = Perfil.objects.filter(user__groups=3).all(),
		label="Jefe de Seguridad", empty_label = "Seleccione un jefe de seguridad..."
		)

	class Meta:
		model = Servicio
		exclude = ('cliente',)



class AsignarGuardiaForm(ModelForm):
	"""!
	Clase del formulario para la asignación de guardias

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 24-10-2017
	"""

	def __init__(self, *args, **kwargs):
		"""!
		Metodo que sobreescribe cuando se inicializa el formulario

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 24-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param args <b>{list}</b> Lista de los argumentos
		@param kwargs <b>{dict}</b> Diccionario con argumentos
		@return Retorna el formulario validado
		"""
		super(AsignarGuardiaForm, self).__init__(*args, **kwargs)
		self.fields['pariente'].widget.attrs.update({'class': 'form-control',
		'placeholder': 'Asignar paciente'})
		self.fields['pariente'].queryset = Perfil.objects.filter(user__groups__name="Cliente").all()
		self.fields['notificacion'].label = "¿Recibir notificaciones?"

	class Meta:
		model = SeguridadJefeHijo
		exclude = ('jefe_seguridad',)

class AsignarGuardiaExcludeForm(AsignarGuardiaForm):
	"""!
	Clase del formulario para la asignación de guardias

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 24-10-2017
	"""

	def __init__(self, *args, **kwargs):
		"""!
		Metodo que sobreescribe cuando se inicializa el formulario

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 24-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@param args <b>{list}</b> Lista de los argumentos
		@param kwargs <b>{dict}</b> Diccionario con argumentos
		@return Retorna el formulario validado
		"""
		super(AsignarGuardiaExcludeForm, self).__init__(*args, **kwargs)
		asignados = SeguridadJefeHijo.objects.values_list('pariente_id')
		self.fields['pariente'].queryset = Perfil.objects.exclude(id__in=asignados).filter(user__groups__name="Cliente").all()
		

AsignarGuardiaFormset = inlineformset_factory(Perfil,SeguridadJefeHijo, 
	form=AsignarGuardiaExcludeForm,
	extra=0,
	min_num=1, 
	validate_min=True, 
	fk_name="jefe_seguridad",
	fields=("pariente","notificacion")
	)