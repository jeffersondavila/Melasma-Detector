# Generated by Django 4.2.4 on 2023-10-07 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0004_enfermedad_paciente_historialclinico_analisis'),
    ]

    operations = [
        migrations.AddField(
            model_name='enfermedad',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
