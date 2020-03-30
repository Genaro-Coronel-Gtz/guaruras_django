import django_filters
from django import forms
from .models import Alerta

class AlertaFilter(django_filters.FilterSet):

	username = django_filters.CharFilter(name='usuario__user__username' ,label='Nombre de Usuario',
		lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control'}))

	rango_fecha = django_filters.DateFromToRangeFilter(name='fecha' ,label='Fecha',widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control'}))
	
	class Meta:
		model = Alerta
		fields = ['username','rango_fecha']