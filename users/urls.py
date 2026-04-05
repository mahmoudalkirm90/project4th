from django.urls import path
from .views import *
from .views import UserLoginView 
urlpatterns = [
   path('login/', UserLoginView.as_view(), name='user-login'),
   path('otp/resend', ResendOtpView.as_view(), name='resend-otp'),
   path('otp/verify', VerifyOtpView.as_view(), name='verify-otp'),
]