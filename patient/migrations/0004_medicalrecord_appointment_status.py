# Generated by Django 5.0.7 on 2024-08-03 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_alter_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrecord',
            name='appointment_status',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='has_status', to='patient.appointment'),
            preserve_default=False,
        ),
    ]
