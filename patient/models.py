from django.db import models
from users.models import User
PENDING,SCHEDULED,COMPLETED,CANCELED = ('pending','scheduled','completed','canceled')

class Appointment(models.Model):
    STATUS_APP = (
        (PENDING,PENDING),
        (SCHEDULED,SCHEDULED), 
        (COMPLETED,COMPLETED), 
        (CANCELED,CANCELED),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='appointments_as_doctor', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_APP,default=PENDING)

    def __str__(self):
        return f"{self.user.username} with {self.doctor.username} on {self.appointment_date}"


    #Medical Record Model
class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='medical_records_as_doctor', on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    appointment_status = models.ForeignKey(Appointment,on_delete=models.CASCADE,related_name='has_status',null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Medical record for {self.user.username} by {self.doctor.username} on {self.record_date}"

class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='prescriptions_as_doctor', on_delete=models.CASCADE)
    prescription_date = models.DateTimeField(auto_now_add=True)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    instructions = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.user.username} by {self.doctor.username} on {self.prescription_date}"
