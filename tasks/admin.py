from django.contrib import admin
from .models import Paciente, HistorialClinico, Enfermedad, Analisis, History, Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )

admin.site.register(Task, TaskAdmin)
admin.site.register(History)
admin.site.register(Paciente)
admin.site.register(HistorialClinico)
admin.site.register(Enfermedad)
admin.site.register(Analisis)