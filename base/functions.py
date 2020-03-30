from django.contrib.auth.models import User
from servicios.models import SeguridadServicio, SeguridadJefeHijo

def validate_email(email):
    """!
    Función que permite validar el email

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 20-04-2017
    @param email {str} Recibe el email
    @return Devuelve verdadero o falso
    """
    
    email = User.objects.filter(email=email)
    if email:
        return True
    else:
        return False


def get_seguridad_servicios(id_servicio):
    """!
    Función que retorna los guardias asignados en una tupla

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 16-10-2017
    @param id_servicio {int} Recibe id del servicio
    @return Devuelve una tupla con los datos
    """

    lista = ('', '---------'),

    try:
        for guardias in SeguridadServicio.objects.filter(servicio_id=int(id_servicio)):
            lista += (guardias.guardia.id , guardias.guardia.user.username ),
    except Exception as e:
        pass
    return lista

def get_jefe_user(servicio_id,perfil):
    """!
    Función que retorna el listado de los jefes de seguridad
    y sus parientes asignados a un servicio

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 01-11-2017
    @param id_servicio {int} Recibe id del servicio
    @param perfil {object} Recibe el objeto del perfil a excluir
    @return Devuelve una lista con los datos
    """
    if perfil.user.groups.first().id == 2:
        seguridad = SeguridadServicio.objects.filter(servicio_id=servicio_id)
    else:
        seguridad = SeguridadServicio.objects.filter(guardia_id=perfil.id)

    seguridad = seguridad.exclude(guardia__is_online=False,guardia__onesignal_id=None)

    listado_seguridad = seguridad.values_list('guardia__id',flat=True)

    onesignal_ids = [x for x in seguridad.exclude(guardia_id=perfil.id)\
    .values_list('guardia__onesignal_id',flat=True)]

    listado_parientes = SeguridadJefeHijo.objects.filter(
        jefe_seguridad_id__in=listado_seguridad,
        pariente__is_online=True,
        notificacion=True
    ).exclude(pariente__onesignal_id=None)

    if listado_parientes:
        listado_parientes = listado_parientes.exclude(pariente_id=perfil.id).values_list('pariente__onesignal_id',flat=True)
        onesignal_ids += [item for item in listado_parientes]
    return onesignal_ids
