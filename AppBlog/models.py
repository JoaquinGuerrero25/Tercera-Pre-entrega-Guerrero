from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Publicaciones(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='publicaciones_imagenes', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    def _str__(self):
        return self.titulo

class Editar(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_edicion = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f'{self.publicacion.titulo} - {self.fecha_edicion}'

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicaciones, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f'{self.autor.username} - {self.fecha_comentario}'