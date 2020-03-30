from django.db import models
from usuarios.models import Perfil
from base.constant import TIPO_ALERTAS
from servicios.models import Servicio

class Alerta(models.Model):
	"""
	Clase que gestiona el modelo de alertas

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 11-10-17
	"""

	# Tipo de la alerta
	tipo = models.CharField(max_length=2,choices=TIPO_ALERTAS)

	# Latitud de la alerta
	latitud = models.CharField(max_length=50)

	# Longitud de la alerta
	longitud = models.CharField(max_length=50)

	# Ubicación de la alerta
	ubicacion = models.CharField(max_length=255)

	# Usuario que envía la alerta
	usuario = models.ForeignKey(Perfil)

	# Si la alerta fue atendida
	atendida = models.BooleanField(default=False)

	# Fecha de envio de la alerta
	fecha = models.DateTimeField(auto_now=True)

	# Relación con el servicio
	servicio = models.ForeignKey(Servicio)

	def __str__(self):
		"""!
		Metodo que muestra el objeto alerta como un str

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 17-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@return Retorna el str de la alerta
		"""
		return str("Alerta - "+self.usuario.user.username+" ")+str(self.fecha)
