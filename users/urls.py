from django.urls import path
from .views import *
from .views import UserLoginView 
urlpatterns = [
   path('verify-otp/', verify_otp, name='verify-otp'),
   path('login/', UserLoginView.as_view(), name='user-login'),
]