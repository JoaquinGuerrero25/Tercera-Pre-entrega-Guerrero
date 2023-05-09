from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Publicaciones, Editar, Comentario

class Registrar_Usuario(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
class Iniciar_Sesion(AuthenticationForm):
    pass

class Formulario_Publicacion(forms.ModelForm):
    imagen = forms.ImageField(required=False)
    class Meta:
        model = Publicaciones
        fields = ['titulo', 'contenido', 'imagen'] 

class Formulario_Editar(forms.ModelForm):
    class Meta:
        model = Editar
        fields = ('contenido',)
        labels = {'contenido': 'Contenido'}

class Formulario_Comentarios(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('contenido',)
        labels = {'contenido': 'Contenido del comentario'}


class Formulario_busqueda(forms.Form):
    autor = forms.CharField(required=True, label='Nombre del autor', max_length=100)