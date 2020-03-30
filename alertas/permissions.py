from rest_framework import permissions
from usuarios.models import Perfil

class HasUserAlertasPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS) and (request.method == "GET" or request.method == "POST"):
            user = request.user
            perfil = Perfil.objects.filter(user=user).first()
            return obj.usuario == perfil# or request.user.is_superuser
        return False

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS) and (request.method == "GET" or request.method == "POST"):
            return True
        return False
