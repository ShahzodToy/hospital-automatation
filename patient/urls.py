from django.urls import path
from .views import *

urlpatterns = [
    path('list-doctors/',ListDoctors.as_view()),
    path('make-appointment/',CreateAppointmnet.as_view()),
    path('appointments/',DeleteListAppointments.as_view()),
    path('appointments/<int:pk>',DeleteListAppointments.as_view()),
]