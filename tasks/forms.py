from .models import Task, Paciente, Enfermedad
from django import forms
from django.forms import ModelForm

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class PatientForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'fecha_nacimiento', 'informacion_adicional']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del paciente'}),
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class DiseaseForm(ModelForm):
    class Meta:
        model = Enfermedad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la enfermedad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }