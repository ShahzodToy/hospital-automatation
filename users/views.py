from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.views import APIView
from .serializers import *
from .models import User,CODE_VERIFIED,NEW
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UsersignupView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserRegistrationSerializer

class VerifyCodeView(APIView):
    permission_classes = (IsAuthenticated, )


    def post(self,request,*args,**kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        
        

        self.verify_code(user,code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh']
            }
        )
    
    @staticmethod
    def verify_code(user,code):
        verifies =  user.verify_code.filter(exparition_time__gte=datetime.now(),code=code,is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class ChangeUserInfoView(UpdateAPIView):
    serializer_class = ChangeUserInfoSerializer
    permission_classes = (IsAuthenticated, )
    

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInfoView,self).update(request,*args,**kwargs)
        data = {
            'success':'True',
            'message':'User saved successfully'
        }
        return Response(data)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer