from django.urls import path
from .views import *
from .views import UserLoginView 
urlpatterns = [
   path('otp/verify', verify_otp, name='verify-otp'),
   path('login/', UserLoginView.as_view(), name='user-login'),
   path('otp/resend', ResendOtpView.as_view(), name='resend-otp'),
   path('otp/verify', VerifyOtpView.as_view(), name='verify-otp'),
]