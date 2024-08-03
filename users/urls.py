from django.urls import path
from .views import *


urlpatterns = [
    path('signup/',UsersignupView.as_view()),
    path('verify/',VerifyCodeView.as_view()),
    path('update-info/',ChangeUserInfoView.as_view()),
    path('login/',LoginView.as_view())
]