from typing import Any
from rest_framework import serializers
from .models import User,CODE_VERIFIED,DONE,NEW
# from .utility import send_email
from .task import send_email
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args,**kwargs):
        super(UserRegistrationSerializer,self).__init__(*args,**kwargs)
        self.fields['input_email'] = serializers.CharField(required=False)
        

    class Meta:
        model=User
        fields = ('id','auth_status')
        extra_kwargs = {
            'auth_status':{'read_only':True,'required':False}
        }

    def validate(self, data):
        super(UserRegistrationSerializer,self).validate(data)

        data = self.auth_validate(data)
        return data
    
    @staticmethod
    def auth_validate(data):
        print(data)
        user_input = str(data.get('input_email')).lower()
        if user_input:
            data = {
                'email':user_input,     
            }
        else: 
            data = {
                'status':False
            }
            raise ValidationError(data)
        
        return data

    def validate_input_email(self,valid):
        valid = valid.lower()
        if valid and User.objects.filter(email = valid).exists():
            data = {
                'status':False,
                'message':'Bu emaildan odgdin foydalanilgan'
            }
            raise ValidationError(data)
        
        
        return valid
    
    def create(self, validated_data):
        user = super(UserRegistrationSerializer,self).create(validated_data)
        code = user.genearate_code()
        send_email.delay(user.email,code)
        user.save()
        return user
    
    def to_representation(self, instance):
        data = super(UserRegistrationSerializer,self).to_representation(instance)
        data.update(instance.token())
        return data
        
        
class ChangeUserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True,required=True)
    last_name = serializers.CharField(write_only=True,required=True)
    username = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)
    confirm_password=serializers.CharField(write_only=True,required=True)

    def validate_first_name(self,data):
        if len(data)<5 and len(data) > 35:
            raise ValidationError({'message':'First name must be between 5 and 35 length'})
        if data.isdigit():
            raise ValidationError({'Firts name must be as string'})
        return data
    
    def validate_last_name(self,data):
        if len(data)<5 and len(data) > 35:
            raise ValidationError({'message':'First name must be between 5 and 35 length'})
        if data.isdigit():
            raise ValidationError({'Last name must be as string'})
        return data
    
    def validate_username(self,data):
        if len(data)<5 and len(data) > 35:
            raise ValidationError({'message':'username  must be between 5 and 35 length'})
        if data.isdigit():
            raise ValidationError({'username must be as string'})
        return data
    
    def validate(self,data):
        password = data.get('password',None)
        confirm_password = data.get('confirm_password',None)

        if password != confirm_password:
            raise ValidationError({'message':'Your password does not matched'})
        if password:
            validate_password(password)
            validate_password(confirm_password)
        return data
        
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.username = validated_data.get('username',instance.username)
        instance.password = validated_data.get('password',instance.password)

        if validated_data['password']:
            instance.set_password(validated_data.get('password',instance.password))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
        instance.save()

        return instance
    
class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args,**kwargs):
        super(LoginSerializer,self).__init__(*args,**kwargs)
        self.fields['username'] = serializers.CharField(required=True)
        

    
    def auth_validate(self,data):
        username = data.get('username',None)

        self.get_user(username__iexact = username)

        current_user = User.objects.filter(username__iexact=username).first()
        if current_user is not None and current_user.auth_status  in [CODE_VERIFIED,NEW]:
            raise ValidationError({"message":"user not found"})
        user= authenticate(username=username,password = data['password'])

        if user is not None:
            self.user = user
        else:
            raise ValidationError({'message':"Sorry, login or password you entered is incorrect. Please check and trg again!"})

        return data
    
    def validate(self,data):
        self.auth_validate(data)
        data = self.user.token()

        data['status'] = self.user.auth_status
        return data
        

    def get_user(self,**kwargs):
        user = User.objects.filter(**kwargs)
        if not user.exists():
            raise ValidationError({'message':"User not found"})
        return user.first()

        


