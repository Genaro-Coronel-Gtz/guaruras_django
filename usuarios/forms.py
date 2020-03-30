from django import forms
from django.forms import ModelForm
from django.core.validators import MinValueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.fields import (
    CharField, BooleanField
)
from django.forms.widgets import (
    PasswordInput, CheckboxInput, Select
)
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Perfil
from base.functions import validate_email

class LoginForm(forms.Form):
    """!
    Clase del formulario de logeo

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 01-03-2017
    """
    ## Campo de la constraseña
    contrasena = CharField()

    ## Nombre del usuario
    usuario = CharField()

    ## Formulario de recordarme
    remember_me = BooleanField()


    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['contrasena'].widget = PasswordInput()
        self.fields['contrasena'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Contraseña'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Nombre de Usuario'})
        self.fields['remember_me'].label = "Recordar"
        self.fields['remember_me'].widget = CheckboxInput()
        self.fields['remember_me'].required = False

    def clean(self):
        """!
        Método que valida si el usuario a autenticar es valido

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 21-04-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con los errores
        """
        usuario = self.cleaned_data['usuario']
        contrasena = self.cleaned_data['contrasena']
        usuario = authenticate(username=usuario,password=contrasena)
        if(not usuario):
            msg = "Verifique su usuario o contraseña"
            self.add_error('usuario', msg)

    class Meta:
        fields = ('usuario', 'contrasena', 'remember_me')


class UserRegisterForm(UserCreationForm):
    """!
    Formulario de Registro

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 20-04-2017
    """
    def __init__(self, *args, **kwargs):
        """!
        Metodo que sobreescribe cuando se inicializa el formulario

        @author Rodrigo Boet (rudmanmrrod at gmail)
        @copyright GNU/GPLv2
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param args <b>{list}</b> Lista de los argumentos
        @param kwargs <b>{dict}</b> Diccionario con argumentos
        @return Retorna el formulario validado
        """
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Nombre de usuario'})
        self.fields['username'].required = True
        self.fields['username'].label = "Nombre de Usuario"
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Contraseña'})
        self.fields['password1'].required = True
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Repite la Contraseña'})
        self.fields['password2'].required = True
        self.fields['password2'].label = "Repita su contraseña"
        self.fields['email'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Email'})
        self.fields['email'].required = True
        self.fields['email'].label = "Correo"

    ## nombre de la empresa
    nombre_empresa = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Nombre de la Empresa'}),
        label="Nombre de la Empresa"
        )

    ## Tipo de Usuario
    group = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class':'form-control','onchange':'register_show(this.value)'}),
        label="Tipo de Usuario", queryset=Group.objects.all(),
        empty_label = "Seleccione un tipo de usuario..."
        )

    ## Parte de servicios

    # kilometraje
    kilometraje = forms.FloatField(
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Km'}),
        required = False, validators=[MinValueValidator(1)], label = 'Perimetro'
        )

    # Velocidad
    velocidad = forms.FloatField(
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'Límite de Velocidad (Km/h)'}),
        required = False, validators=[MinValueValidator(1)]
        )

    # Telefono
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Télefono'}),
        required = False
        )

    # Frecuencia de Rastreo
    frecuencia_rastreo = forms.CharField(
        widget = forms.Select(attrs={'class':'form-control'},choices=(('','Seleccione un valor...'),('5','5'),('10','10'),('15','15'),('30','30'))),
        label = "Frecuencia de Rastreo (mínutos)", required = False
        )
     

    # Listado de guardias 
    guardias = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        queryset = Perfil.objects.filter(user__groups=3).all(),
        label="Jefe de Seguridad",required = False,
        empty_label = "Seleccione un jefe de seguridad..."
        )

    # Latitud inicial
    latitud_inicial = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Latitud','readonly':True}),
        required = False
        )

    # Longitud
    longitud_inicial = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Longitud','readonly':True}),
        required = False
        )

    # Notificación
    notificacion = forms.BooleanField(required = False, label="¿Recibir Notificaciones?")


    def clean_email(self):
        """!
        Método que valida si el correo es única
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 01-03-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        email = self.cleaned_data['email']
        if(validate_email(email)):
            raise forms.ValidationError("El correo ingresado ya existe")
        return email

    def clean_kilometraje(self):
        """!
        Método que valida el kilometraje
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 08-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        kilometraje = self.cleaned_data['kilometraje']
        if(group.id!=1 and kilometraje==''):
            raise forms.ValidationError("Este campo es requerido")
        return kilometraje

    def clean_velocidad(self):
        """!
        Método que valida la velocidad
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 14-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        velocidad = self.cleaned_data['velocidad']
        if(group.id!=1 and velocidad==''):
            raise forms.ValidationError("Este campo es requerido")
        return velocidad

    def clean_telefono(self):
        """!
        Método que valida el telefono
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 08-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        telefono = self.cleaned_data['telefono']
        if(group.id!=1 and telefono==''):
            raise forms.ValidationError("Este campo es requerido")
        return telefono

    def clean_frecuencia_rastreo(self):
        """!
        Método que valida el frecuencia de rastreo
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 08-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        frecuencia_rastreo = self.cleaned_data['frecuencia_rastreo']
        if(group.id!=1 and frecuencia_rastreo==''):
            raise forms.ValidationError("Este campo es requerido")
        return frecuencia_rastreo

    def clean_latitud_inicial(self):
        """!
        Método que valida la latitud inicial
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 14-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        latitud_inicial = self.cleaned_data['latitud_inicial']
        if(group.id!=1 and latitud_inicial==''):
            raise forms.ValidationError("Este campo es requerido")
        return latitud_inicial

    def clean_longitud_inicial(self):
        """!
        Método que valida la longitud inicial
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 14-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        longitud_inicial = self.cleaned_data['longitud_inicial']
        if(group.id!=1 and longitud_inicial==''):
            raise forms.ValidationError("Este campo es requerido")
        return longitud_inicial

    def clean_guardias(self):
        """!
        Método que valida los guardias
    
        @author Rodrigo Boet (rudmanmrrod at gmail)
        @date 12-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @return Retorna el campo con la validacion
        """
        group = self.cleaned_data['group']
        guardias = self.cleaned_data['guardias']
        if(group.id==2 and (guardias=='' or guardias is None)):
            raise forms.ValidationError("Es necesario seleccionar un jefe de seguridad")
        return guardias


    class Meta:
        model = User
        exclude = ['is_staff','is_active','date_joined','password']


class PasswordResetForm(PasswordResetForm):
    """!
    Clase del formulario de resetear contraseña

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @date 02-05-2017
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Correo'})

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get("email")

        if email:
            msg = "Error no existe el email"
            try:
                User.objects.get(email=email)
            except:
                self.add_error('email', msg)



class PasswordConfirmForm(SetPasswordForm):
    """!
    Formulario para confirmar la constraseña

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-05-2017
    """
    def __init__(self, *args, **kwargs):
        super(PasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Contraseña Nueva'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Repita su Contraseña'})



class UserUpdateForm(forms.ModelForm):
    """!
    Formulario de Actualizacion

    @author Rodrigo Boet (rudmanmrrod at gmail)
    @date 15-11-2017
    """

    ## Nombre de Usuario
    username = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Nombre de usuario',
            'disabled':True}),
        label="Nombre de Usuario",required=False
        )

    ## Correo
    email = forms.EmailField(max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Nombre de usuario'}),
        label="Email"
        )

    ## nombre de la empresa
    nombre_empresa = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Nombre de la Empresa'}),
        label="Nombre de la Empresa"
        )


    class Meta:
        model = User
        exclude = ['is_staff','is_active','date_joined','password']
