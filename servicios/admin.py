from django.contrib import admin
from .models import Servicio, SeguridadServicio, SeguridadJefeHijo

admin.site.register(Servicio)
admin.site.register(SeguridadServicio)
admin.site.register(SeguridadJefeHijo)

