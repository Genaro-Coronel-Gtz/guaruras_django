from django import forms
from usuarios.models import Perfil

class SendNotificationForm(forms.Form):
	"""!
	Clase del formulario de creación de notificaciones

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 18-10-2017
	"""
	# Listado de guardias 
	guardias_list = forms.ModelMultipleChoiceField(
		widget=forms.CheckboxSelectMultiple(),
		queryset = Perfil.objects.filter(user__groups=3).exclude(onesignal_id=None).all(),
		label='Listado de Guardias')