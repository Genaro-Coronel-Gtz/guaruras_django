from rest_framework import permissions
from usuarios.models import Perfil

class HasUserServicioPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            perfil = Perfil.objects.filter(user=user).first()
            return obj.cliente == perfil or request.user.is_superuser

