from django.forms.models import BaseModelForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import Registrar_Usuario, Iniciar_Sesion, Formulario_Publicacion, Formulario_Comentarios, Formulario_busqueda
from .models import Publicaciones, Editar, Comentario
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

def lista_publicaciones(request): 
    publicacion = Publicaciones.objects.all()
    if publicacion:
        context = {'publicacion':publicacion}
        return render(request, 'AppBlog/lista_publicaciones.html',context=context)
    else:
        mensaje = 'No se han creado publicaciones.'
        context = {'mensaje':mensaje}
        return render(request, 'AppBlog/lista_publicaciones.html',context=context)

def detalle_publicacion(request, pk):
    publicacion = get_object_or_404(Publicaciones, pk=pk)
    es_creador = publicacion.autor == request.user
    comentarios = Comentario.objects.filter(publicacion=publicacion).order_by('-fecha_comentario')
    return render(request, 'AppBlog/detalle_publicacion.html', {'publicacion': publicacion, 'es_creador': es_creador, 'comentarios': comentarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = Registrar_Usuario(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error('username', 'El nombre de usuario ya existe')
            else:
                usuario = form.save()
                usuario_autenticado = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                login(request, usuario_autenticado)
                return redirect('lista_publicaciones')
    else:
        form = Registrar_Usuario()
    return render(request, 'AppBlog/crear_usuario.html', {'form':form})


class iniciar_sesion(LoginView):
    template_name = 'AppBlog/iniciar_sesion.html'
    authentication_form = Iniciar_Sesion
    success_url = reverse_lazy('lista_publicaciones')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)

def cerrar_sesion(request):
    logout(request)
    return redirect('lista_publicaciones')

class Crear_Publicacion(LoginRequiredMixin, CreateView):
    model = Publicaciones
    form_class = Formulario_Publicacion
    success_url = reverse_lazy('lista_publicaciones')
    template_name = 'AppBlog/crear_publicacion.html'
    
    def form_valid(self, form):
        form.instance.autor =self.request.user
        return super().form_valid(form)

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicaciones, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = Formulario_Publicacion(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            Editar.objects.create(publicacion=publicacion, contenido=publicacion.contenido)
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        form = Formulario_Publicacion(instance=publicacion)
    return render(request, 'AppBlog/editar_publicacion.html', {'form': form})

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicaciones, pk=pk, autor=request.user)
    if request.method == 'POST':
        publicacion.delete()
        return redirect('lista_publicaciones')
    return render(request, 'eliminar_publicacion.html', {'publicacion': publicacion})

@login_required
def agregar_comentario(request, publicacion_id):
    publicacion = Publicaciones.objects.get(id=publicacion_id)
    if request.method == 'POST':
        formulario = Formulario_Comentarios(request.POST)
        if formulario.is_valid():
            comentario = formulario.save(commit=False)
            comentario.publicacion = publicacion
            comentario.autor = request.user
            comentario.save()
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        formulario = Formulario_Comentarios()
    return render(request, 'AppBlog/detalle_publicacion.html', {'formulario': formulario, 'publicacion': publicacion})


def buscar_titulo(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if not query:
            mensaje = "Debe ingresar una palabra clave para buscar"
            return render(request, 'AppBlog/buscar_por_titulo.html', {'mensaje': mensaje})
        else:
            publicaciones = Publicaciones.objects.filter(titulo__icontains=query)
            if publicaciones.exists():
                return render(request, 'AppBlog/resultado_busqueda.html', {'publicaciones': publicaciones})
            else:
                mensaje = f"No se encontraron publicaciones con la palabra clave '{query}' en el título"
                return render(request, 'AppBlog/buscar_por_titulo.html', {'mensaje': mensaje})