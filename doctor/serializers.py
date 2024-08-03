from rest_framework import serializers
from patient.models import SCHEDULED,CANCELED,MedicalRecord,Prescription,COMPLETED
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError


class ChangeDoctorInfo(serializers.Serializer):
    phone_number = serializers.CharField(required=True,write_only=True)
    address = serializers.CharField(required=True,write_only=True)
    city = serializers.CharField(required=True,write_only=True)
    state = serializers.CharField(required=True,write_only=True)
    postal_code = serializers.CharField(required=True,write_only=True)
    medical_license_number = serializers.CharField(required=True,write_only=True)
    specialization = serializers.CharField(required=True,write_only=True)
    department = serializers.CharField(required=True,write_only=True)
    insurance_info = serializers.CharField(required=True,write_only=True)
    emergency_contact = serializers.CharField(required=True,write_only=True)
    

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number',instance.phone_number)
        instance.city = validated_data.get('city',instance.city)
        instance.state = validated_data.get('state',instance.state)
        instance.postal_code = validated_data.get('postal_code',instance.postal_code)
        instance.medical_license_number = validated_data.get('medical_license_number',instance.medical_license_number)
        instance.specialization = validated_data.get('specialization',instance.specialization)
        instance.department = validated_data.get('department',instance.department)
        instance.insurance_info = validated_data.get('insurance_info',instance.insurance_info)
        instance.emergency_contact = validated_data.get('emergency_contact',instance.emergency_contact)
        instance.save()
        return instance
    

class UpdateAppointment(serializers.Serializer):
    reason = serializers.CharField(write_only=True,required=False)
    status = serializers.CharField(required=True)

    def validate_status(self,status):
        if status not in [SCHEDULED,CANCELED]:
            raise ValidationError({'message':'You must choose on of them ok or not'})
        return status

    def update(self, instance, validated_data):
        instance.reason = validated_data.get('reason',instance.reason)

        if validated_data['status'] == SCHEDULED:
            instance.status = SCHEDULED
        elif validated_data['status'] == CANCELED:
            instance.status = CANCELED
        instance.save()
        return instance
    

class CreateMedicalRecodr(serializers.ModelSerializer):

    class Meta:
        model = MedicalRecord
        fields = ('diagnosis','treatment','notes','notes',"appointment_status")

    def create(self, validated_data):
        appointment = validated_data.get('appointment_status')
        if appointment:
            appointment.status = COMPLETED
            appointment.save()
        medical_record = MedicalRecord.objects.create(**validated_data)
        return medical_record
    
    # def update(self, instance, validated_data):
    #     medical = super(CreateMedicalRecodr,self).update(instance, validated_data)
    #     medical.has_status.status = COMPLETED
    #     medical.save
    #     return medical


    # def get_user(self,**kwargs):
    #     user = User.objects.filter(**kwargs)
    #     if not user.exists():
    #         return ValidationError(
    #             {
    #                 'message':'User not found'
    #             }
    #         )
    #     return user.first()


class CreatePerscription(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = ('medication','dosage','instructions')


    def create(self, validated_data):
        prescription = Prescription.objects.create(**validated_data)
        return prescription
    