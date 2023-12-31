# Generated by Django 4.2.4 on 2023-10-06 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateTimeField()),
                ('informacion_adicional', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialClinico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('notas', models.TextField(blank=True, null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.paciente')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_imagen', models.CharField(max_length=255)),
                ('resultado', models.CharField(max_length=1000)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('enfermedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.enfermedad')),
                ('historial_clinico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.historialclinico')),
            ],
        ),
    ]
