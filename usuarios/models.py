from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
	"""!
	Clase que gestiona el modelo perfil de usuario

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 11-10-17
	"""

	# Nombre de la empresa
	nombre_empresa = models.CharField(max_length=80)

	# Id del usuario en onesignal
	onesignal_id = models.CharField(max_length=50,null=True, blank=True)

	# Campo para el número de télefono
	# telefono = models.CharField(max_length=50, blank=True, null=True)

	# Relación con el usuario
	user = models.OneToOneField(User)
	is_online = models.BooleanField(default=False)
	# telefono = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		"""!
		Metodo que muestra el objeto perfil como un str

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 13-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@return Retorna el str del perfil
		"""
		return str(self.user.username)

from servicios.models import Servicio

class Ubicacion(models.Model):
	"""
	Clase que gestiona la localización enviada por la app

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 11-10-17
	"""

	# Latitud de la ubicación
	latitud = models.CharField(max_length=50)

	# Longitud de la ubicación
	longitud = models.CharField(max_length=50)

	# Fecha y tiempo de envío
	fecha = models.DateTimeField(auto_now=True)

	# Usuario del que se rastrea la ubicación
	usuario = models.ForeignKey(Perfil)

	formatted_address = models.CharField(max_length=250, blank=True, null=True)

	# Relación con el servicio
	# servicio = models.ForeignKey(Servicio, blank=True, null=True)

	def __str__(self):
		"""!
		Metodo que muestra el objeto alerta como un str

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 17-10-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@return Retorna el str del alerta
		"""
		return str("Ubicación - "+self.usuario.user.username+" ")+str(self.fecha)

class Mensaje(models.Model):
	"""
	Clase que los mensajes enviados

	@author Rodrigo Boet (rudmanmrrod at gmail)
	@date 12-11-17
	"""
	# Cuerpo del mensaje
	mensaje = models.TextField()

	# Usuario que envía el mensaje
	usuario = models.ForeignKey(Perfil)

	# Fecha de envio del mensaje
	fecha = models.DateTimeField(auto_now=True)

	def __str__(self):
		"""!
		Metodo que muestra el objeto mensaje como un str

		@author Rodrigo Boet (rudmanmrrod at gmail)
		@date 12-11-2017
		@param self <b>{object}</b> Objeto que instancia la clase
		@return Retorna el str del mensaje
		"""
		return str("Mensaje - "+self.usuario.user.username+" ")+str(self.fecha)