from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_nacimiento = models.DateTimeField()
    informacion_adicional = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class HistorialClinico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente} - {self.usuario}"

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Analisis(models.Model):
    historial_clinico = models.ForeignKey(HistorialClinico, on_delete=models.CASCADE)
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    nombre_imagen = models.CharField(max_length=255)
    resultado = models.CharField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_imagen} - {self.enfermedad}"

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username

class History(models.Model):
    image_name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.image_name + ' - ' + self.user.username