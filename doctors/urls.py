from django.urls import path
from .views import DoctorRegisterView

urlpatterns = [
    path('register/', DoctorRegisterView.as_view(), name='doctor-register'),
]

