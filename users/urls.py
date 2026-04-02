from django.urls import path
from .views import *
from .views import UserLoginView 
urlpatterns = [
   path('otp/verify', verify_otp, name='verify-otp'),
   path('login/', UserLoginView.as_view(), name='user-login'),
   path('otp/resend', resend_otp, name='resend-otp'),
]