from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.generics import *
from .serializers import *
from users.models import User
from rest_framework.response import Response
from .models import Appointment
from rest_framework import status


class ListDoctors(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,*args,**kwargs):
        doctors = User.objects.filter(user_type='doctor')
        data = {}

        for doctor in doctors:
            specialization = doctor.specialization
            if specialization not in data:
                data[specialization] = []
            doctor_info = {
                'username': doctor.username,
                'first_name': doctor.first_name,
                'last_name': doctor.last_name,
                'phone_number': doctor.phone_number,
                'email': doctor.email,
                'country': doctor.country,
            }
            data[specialization].append(doctor_info)
        return Response(data)
    

class CreateAppointmnet(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = MakeAppointment
    permission_classes = (IsAuthenticated, )


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class DeleteListAppointments(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self,request,*args,**kwargs):
        list_of_app = Appointment.objects.filter(user=self.request.user)
        if not list_of_app.exists():
            return Response(
                {
                    'message':"You do not have any appointments"
                }
            )
        data = {
            'Appointments':list(list_of_app.values())
        }
        return Response(data)
    
    def delete(self,request,pk):
        appointment = get_object_or_404(Appointment, id=pk, user=self.request.user)
        appointment.delete()
        return Response(
            {'message': "Appointment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )