from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime,timedelta
import random



NEW,CODE_VERIFIED,DONE = 'new','code_verified','done'
PATIENT,DOCTOR,ADMIN = 'patient','doctor','admin'
class User(AbstractUser):
    AUTH_STATUS = (
        (NEW,NEW),
        (CODE_VERIFIED,CODE_VERIFIED),
        (DONE,DONE)
    )
    USER_TYPE = (
        (PATIENT,PATIENT),
        (DOCTOR,DOCTOR),
        (ADMIN,ADMIN)
    )

    auth_status = models.CharField(choices=AUTH_STATUS,default=NEW,max_length=50)
    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=USER_TYPE,default=PATIENT,max_length=50)
    phone_number = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Healthcare-Specific Information
    medical_license_number = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    insurance_info = models.JSONField(blank=True, null=True)
    emergency_contact = models.JSONField(blank=True, null=True)
    appointments = models.ForeignKey('patient.Appointment',on_delete=models.CASCADE,related_name='has_appointment',null=True)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f'{self.username} as {self.user_type}'
    

    def check_username(self):
        if not self.username:
            temp_username = f"normal-user-{uuid.uuid4().__str__().split('-')[-1]}"
            self.username = temp_username

    def check_pass(self):
        if not self.password:
            temp_password = f"normal-user-password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access':str(refresh.access_token),
            'refresh':str(refresh)
        }
    def check_emial(self):
        if self.email:
            temp_email = self.email.lower()
            self.email = temp_email
    
    def hashing_password(self): # it will hash regular passwords
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def save(self,*args,**kwargs):
        self.clean()
        super(User,self).save(*args,**kwargs)

    def clean(self):
        self.check_username()
        self.hashing_password()
        self.check_pass()
        self.check_emial()

    def genearate_code(self):
        code = ''.join([str(random.randint(0,100)%10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id = self.id,
            code = code
        )
        return code


class UserConfirmation(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='verify_code')
    exparition_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code
    

    def save(self,*args,**kwargs):

        self.exparition_time = datetime.now() + timedelta(minutes=2)

        super(UserConfirmation,self).save(*args,**kwargs)
        