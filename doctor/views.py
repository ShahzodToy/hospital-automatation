from django.shortcuts import render
from .serializers import *
from patient.models import COMPLETED
from patient.models import Appointment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework.generics import *
from rest_framework.permissions import *
from users.models import User

DOCTOR = 'doctor'
class ChangeDoctorInfoView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangeDoctorInfo
    

    def get_object(self):
        if self.request.user.user_type == DOCTOR:
            return self.request.user
        raise PermissionDenied("This section is only for doctors.")

    def update(self, request, *args, **kwargs):
        super(ChangeDoctorInfoView,self).update(request, *args, **kwargs)
        data = {
            'sucess':True,
            'message':"Doctor user information updated successfully"
        }
        return Response(data)

class ListAppointment(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self,request,*args,**kwargs):
        if self.request.user.user_type != DOCTOR:
            raise PermissionDenied("This section is only for doctors.")
        
        try:
            doctor_appointments = Appointment.objects.filter(doctor=self.request.user)
            
            if not doctor_appointments.exists():
                raise Appointment.DoesNotExist
        except Appointment.DoesNotExist:
            return Response({'message': 'This doctor has no appointments'})

        data = {
            'List of appointments for': {
                'appointments': list(doctor_appointments.values())
            }
        }
        
        return Response(data)


class UpdateAppointmentView(UpdateAPIView):
    serializer_class = UpdateAppointment
    permission_classes = (IsAuthenticated, )
    queryset = Appointment.objects.all()

    def get_queryset(self):
        pk = self.kwargs['pk']
        return self.queryset.filter(id=pk)
    

class CreateMedicalRecordView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateMedicalRecodr
    queryset = MedicalRecord.objects.all()
    
    def get_user(self):
        pk = self.kwargs.get('pk')
        user = User.objects.filter(id=pk).first()
        if not user:
            raise ValidationError({'message': 'User not found'})
        return user
    
    def perform_create(self, serializer):
        user = self.get_user()
        serializer.save(user=user, doctor=self.request.user)
        
class CreatePrescriptionView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreatePerscription
    queryset = Prescription.objects.all()

    def get_user(self):
        pk = self.kwargs.get('pk')
        user = User.objects.filter(id=pk).first()
        if not user:
            raise ValidationError({'message': 'User not found'})
        return user
    
    def perform_create(self, serializer):
        user = self.get_user()
        serializer.save(user=user, doctor=self.request.user)
        