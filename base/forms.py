from django import forms
from .models import TerminosCondiciones

class TerminosCondicionesForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(
        attrs={
        'class':'form-control',
        'placeholder':'Texto',
        'rows':'20',
        }
    ))