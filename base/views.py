from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required
from base.models import TerminosCondiciones
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from .forms import TerminosCondicionesForm
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect

def user_super_admin(function):
    def wrap(request, *args, **kwargs):

        user = request.user
        if user.is_superuser:
             return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap


class Inicio(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    """!
    Clase de la vista inicial

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 11-10-2017
    """
    template_name = "inicio.html"
    group_required = u"Administrador"

class TerminosCondicionesFormView(LoginRequiredMixin, FormView):
    """!
    Clase de la vista inicial

    @author Pablo Gonzalez (pdonaire1 at gmail)
    @date 11-10-2017
    """
    template_name = "terminos_condiciones.html"
    # group_required = u"Administrador"
    form_class = TerminosCondicionesForm
    success_url = '/terminos/'#reverse('terminos')

    def form_valid(self, form):
        obj =TerminosCondiciones.objects.get(id=1)
        obj.texto = form.cleaned_data['texto']
        obj.save()
        return super(TerminosCondicionesFormView, self).form_valid(form)

    def get_object(self, queryset=None):
        if TerminosCondiciones.objects.filter(id=1).exists():
            obj =TerminosCondiciones.objects.get(id=1)
        else:
            obj = TerminosCondiciones.objects.create(id=1, texto='')
        return obj

    def get_initial(self):
        context = super(TerminosCondicionesFormView, self).get_initial()
        context['texto'] = TerminosCondiciones.objects.get(id=1).texto
        print (context)
        return context
    def get_context_data(self, **kwargs):
        if TerminosCondiciones.objects.filter(id=1).exists():
            obj =TerminosCondiciones.objects.get(id=1)
        else:
            obj = TerminosCondiciones.objects.create(id=1, texto='')
        context = super(TerminosCondicionesFormView, self).get_context_data(**kwargs)
        context['texto'] = obj.texto
        return context
    
    @method_decorator(user_super_admin)
    def dispatch(self, *args, **kwargs):
        return super(TerminosCondicionesFormView, self).dispatch(*args, **kwargs)


class TerminosCondicionesView(TemplateView):
    template_name = "terminos.html"

    def get_context_data(self, **kwargs):
        context = super(TerminosCondicionesView, self).get_context_data(**kwargs)
        if TerminosCondiciones.objects.filter(id=1).exists():
            obj =TerminosCondiciones.objects.get(id=1)
        else:
            obj = TerminosCondiciones.objects.create(id=1, texto='')
        context['object'] = obj
        context['show_update'] = True if (self.request.user and self.request.user.is_superuser) else False
        return context


class TerminosCondicionesAPIView(APIView):
    """
    @author Pablo Gonzalez (pdonaire1 at gmail)
    @date 11-10-2017
    Muestra los terminos y condiciones del servicio
    """
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        return Response({
            'texto': TerminosCondiciones.objects.get(id=1).texto
        })

