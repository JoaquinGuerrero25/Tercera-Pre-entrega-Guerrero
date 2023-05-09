from django.urls import path
from .views import crear_usuario, iniciar_sesion, lista_publicaciones, cerrar_sesion,Crear_Publicacion, detalle_publicacion, editar_publicacion, eliminar_publicacion, agregar_comentario,buscar_titulo
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',lista_publicaciones, name='lista_publicaciones'),
    path('crear_usuario', crear_usuario, name='crear_usuario'),
    path('iniciar_sesion', iniciar_sesion.as_view(), name='iniciar_sesion'),
    path('crear_publicacion/', Crear_Publicacion.as_view(), name='crear_publicacion'),
    path('detalle/<int:pk>/', detalle_publicacion, name='detalle_publicacion'),
    path('publicacion/<int:pk>/editar/', editar_publicacion, name='editar_publicacion'),
    path('eliminar/<int:pk>/', eliminar_publicacion, name='eliminar_publicacion'),
    path('publicacion/<int:publicacion_id>/agregar_comentario/', agregar_comentario, name='agregar_comentario'),
    path('buscar/titulo/', buscar_titulo, name='buscar_titulo'),
    path('logout/', cerrar_sesion, name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)