from rest_framework import serializers
from .models import Appointment
from users.models import User
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework.response import Response


class MakeAppointment(serializers.ModelSerializer):
    doctor = serializers.CharField()
    appointment_date = serializers.DateTimeField()

    class Meta:
        model = Appointment
        fields = ('appointment_date','doctor','reason','appointment_date')
    
    def validate_doctor(self, username):
        try:
            doctor = User.objects.get(username=username, user_type='doctor')
        except User.DoesNotExist:
            raise ValidationError({'message': "Doctor with this username not found"})
        return doctor.id
    
    
        
    def create(self, validated_data):
        request = self.context['request']
        appointment = Appointment.objects.create(
            user= request.user,
            doctor_id = validated_data.get('doctor'),
            appointment_date = validated_data.get('appointment_date',None),
            reason = validated_data.get('reason',None)
        )
        appointment.save()
        return appointment