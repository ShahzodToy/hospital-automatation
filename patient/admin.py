from django.contrib import admin
from .models import *


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id','reason')

admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)