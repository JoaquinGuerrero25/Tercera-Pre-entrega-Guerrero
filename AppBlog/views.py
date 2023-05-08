from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import Registrar_Usuario, Iniciar_Sesion
from .models import Publicaciones


def lista_publicaciones(request):
    publicacion = Publicaciones.objects.all()
    if len(Publicaciones) == 0:
        mensaje = 'No hay publicaciones creadas.'
    else:
        mensaje = None
    return render(request, 'lista_publicaciones.html', {'publicacion':publicacion, 'mensaje': mensaje})

def crear_usuario(request):
    if request.method == 'POST':
        form = Registrar_Usuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_publicaciones.html')
    else:
        form = Registrar_Usuario()
    return render(request, 'registro_usuario.html', {'form':form})

class iniciar_sesion(LoginView):
    template_name = 'iniciar_sesion.html'
    authentication_form = Iniciar_Sesion
    success_url = reverse_lazy('lista_publicaciones')
