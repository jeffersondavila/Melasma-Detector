from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Task, Paciente, Enfermedad, Analisis, HistorialClinico
from .forms import TaskForm, ImageUploadForm, PatientForm, DiseaseForm, MedicalForm

import os
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image

def home(request):
    return render(request, 'home.html')

# LOG INFORMATION
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})
        login(request, user)
        return redirect('tasks')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

# SHOW INFORMATION
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def patients(request):
    patients = Paciente.objects.filter(user=request.user)
    return render(request, 'patients.html', {"patients": patients})

@login_required
def diseases(request):
    diseases = Enfermedad.objects.filter(user=request.user)
    return render(request, 'diseases.html', {"diseases": diseases})

@login_required
def medicals(request):
    medicals = HistorialClinico.objects.filter(user=request.user)
    return render(request, 'medicals.html', {"medicals": medicals})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def analisis_history(request):
    analisis_list = Analisis.objects.all().order_by('-fecha_creacion')
    return render(request, 'history.html', {'analisis': analisis_list})

# CREATE/UPDATE INFORMATION
@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})

@login_required
def create_patient(request):
    if request.method == "GET":
        return render(request, 'create_patient.html', {"form": PatientForm})
    else:
        try:
            form = PatientForm(request.POST)
            new_patient = form.save(commit=False)
            new_patient.user = request.user
            new_patient.save()
            return redirect('patients')
        except ValueError:
            return render(request, 'create_patient.html', {"form": PatientForm, "error": "Error creating patient."})

@login_required
def create_disease(request):
    if request.method == "GET":
        return render(request, 'create_disease.html', {"form": DiseaseForm})
    else:
        try:
            form = DiseaseForm(request.POST)
            new_disease = form.save(commit=False)
            new_disease.user = request.user
            new_disease.save()
            return redirect('diseases')
        except ValueError:
            return render(request, 'create_disease.html', {"form": DiseaseForm, "error": "Error creating disease."})

@login_required
def create_medical(request):
    if request.method == "GET":
        return render(request, 'create_medical.html', {"form": MedicalForm})
    else:
        try:
            form = MedicalForm(request.POST)
            new_medical = form.save(commit=False)
            new_medical.user = request.user
            new_medical.save()
            return redirect('medicals')
        except ValueError:
            return render(request, 'create_medical.html', {"form": MedicalForm, "error": "Error creating medical history."})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

# DETAIL INFORMATION
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def patient_detail(request, patient_id):
    if request.method == 'GET':
        patient = get_object_or_404(Paciente, pk=patient_id, user=request.user)
        form = PatientForm(instance=patient)
        return render(request, 'patient_detail.html', {'patient': patient, 'form': form})
    else:
        try:
            patient = get_object_or_404(Paciente, pk=patient_id, user=request.user)
            form = PatientForm(request.POST, instance=patient)
            form.save()
            return redirect('patients')
        except ValueError:
            return render(request, 'patient_detail.html', {'patient': patient, 'form': form, 'error': 'Error updating patient.'})

@login_required
def disease_detail(request, disease_id):
    if request.method == 'GET':
        disease = get_object_or_404(Enfermedad, pk=disease_id, user=request.user)
        form = DiseaseForm(instance=disease)
        return render(request, 'disease_detail.html', {'disease': disease, 'form': form})
    else:
        try:
            disease = get_object_or_404(Enfermedad, pk=disease_id, user=request.user)
            form = DiseaseForm(request.POST, instance=disease)
            form.save()
            return redirect('diseases')
        except ValueError:
            return render(request, 'disease_detail.html', {'disease': disease, 'form': form, 'error': 'Error updating disease.'})

@login_required
def medical_detail(request, medical_id):
    if request.method == 'GET':
        medical = get_object_or_404(HistorialClinico, pk=medical_id, user=request.user)
        form = MedicalForm(instance=medical)
        return render(request, 'medical_detail.html', {'medical': medical, 'form': form})
    else:
        try:
            medical = get_object_or_404(HistorialClinico, pk=medical_id, user=request.user)
            form = MedicalForm(request.POST, instance=medical)
            form.save()
            return redirect('medicals')
        except ValueError:
            return render(request, 'medical_detail.html', {'medical': medical, 'form': form, 'error': 'Error updating medical history.'})

# DELETE INFORMATION
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Paciente, pk=patient_id, user=request.user)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients')

@login_required
def delete_disease(request, disease_id):
    disease = get_object_or_404(Enfermedad, pk=disease_id, user=request.user)
    if request.method == 'POST':
        disease.delete()
        return redirect('diseases')

@login_required
def delete_medical(request, medical_id):
    medical = get_object_or_404(HistorialClinico, pk=medical_id, user=request.user)
    if request.method == 'POST':
        medical.delete()
        return redirect('medicals')

# ANALYTICAL LOAD
@login_required
def load_and_prepare_image(img, target_size=(224, 224)):
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.
    return img_array

@login_required
def predict_face(model, img_array):
    predictions = model.predict(img_array)
    return "La imagen no contiene melasma" if predictions[0][0] > 0.5 else "La imagen contiene melasma"

@login_required
def upload_image(request):
    prediction = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            paciente_seleccionado = form.cleaned_data['paciente']
            enfermedad_seleccionada = form.cleaned_data['enfermedad']

            uploaded_image = request.FILES['image'].read()
            img_io = BytesIO(uploaded_image)
            img = image.load_img(img_io, target_size=(224, 224))

            CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(CURRENT_DIR, 'modelo', 'v1_detected.h5')

            model = load_model(model_path)
            img_array = load_and_prepare_image(img)

            prediction = predict_face(model, img_array)

            historial_clinico_paciente = HistorialClinico.objects.filter(paciente=paciente_seleccionado).order_by('-fecha_creacion').first()

            if historial_clinico_paciente:  # Verificar si existe un historial clínico para el paciente
                analisis = Analisis(
                    historial_clinico=historial_clinico_paciente,
                    enfermedad=enfermedad_seleccionada,
                    nombre_imagen=request.FILES['image'].name,
                    resultado=str(prediction)
                )
                analisis.save()
    else:
        form = ImageUploadForm()

    return render(request, 'analyze_image.html', {'form': form, 'prediction': prediction})