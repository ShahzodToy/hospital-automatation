from django.urls import path
from .views import *

urlpatterns = [
    path('change-info/',ChangeDoctorInfoView.as_view()),
    path('list-appointments/',ListAppointment.as_view()),
    path('update-appointment/<int:pk>',UpdateAppointmentView.as_view()),
    path('medical-record/<int:pk>',CreateMedicalRecordView.as_view()),
    path('create-prescription/<int:pk>',CreatePrescriptionView.as_view())
]