from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from usuarios.models import Perfil

class Servicio(models.Model):
    """
    Clase que gestiona el modelo de servicios
    
    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 11-10-17
    """

    # Kilometraje máximo del servicio
    kilometraje = models.FloatField(validators=[MinValueValidator(1)])

    # Velocidad máxima del servicio
    velocidad = models.FloatField(null=True,validators=[MinValueValidator(1)])

    # Número de contacto en caso de emergencia
    telefono = models.CharField(max_length=15,)

    # Frecuencia de envío de información
    frecuencia_rastreo = models.IntegerField(validators=[MinValueValidator(1)])

    # Latitud inicial
    latitud_inicial = models.CharField(max_length=50)

    # Longitud inicial
    longitud_inicial = models.CharField(max_length=50)

    # Relación con el cliente
    cliente = models.OneToOneField(Perfil)

    def __str__(self):
        """!
        Metodo que muestra el objeto perfil como un str

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 13-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el str del perfil
        """
        return str(self.cliente.user.username)

class SeguridadServicio(models.Model):
    """
    Clase intermedia que asigna miembros de seguridad al servicio

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 11-10-17
    """
    
    # Relación con el servicio
    servicio = models.ForeignKey(Servicio)

    # Relación con el guardia
    guardia = models.ForeignKey(Perfil)

    class Meta:
    	unique_together = ('servicio','guardia')

    def __str__(self):
        """!
        Metodo que muestra el objeto perfil como un str

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 13-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el str del perfil
        """
        return str(self.servicio.cliente.user.username+" - "+self.guardia.user.username)


class SeguridadJefeHijo(models.Model):
    """
    Clase intermedia que asigna miembros de seguridad a un servicio
    de un jefe de seguridad

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 24-10-17
    """
    # Relación con el pariente
    pariente = models.ForeignKey(Perfil,related_name="seguridad_jefe_servicio_pariente")

    # Relación con el jefe de seguridad
    jefe_seguridad = models.ForeignKey(Perfil,related_name="seguridad_jefe_servicio_jefe")

    # Envío de notificaciones para el pariente
    notificacion = models.BooleanField(default=False)

    class Meta:
        unique_together = ('pariente','jefe_seguridad')

    def __str__(self):
        """!
        Metodo que muestra el objeto perfil como un str

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 13-10-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el str del perfil
        """
        return str("Jefe: "+self.jefe_seguridad.user.username+" - "+self.pariente.user.username)