from django.urls import path
from .views import DoctorRegisterView , DoctorProfileView , DoctorEducationView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', DoctorRegisterView.as_view(), name='doctor-register'),
    path('profile/update', DoctorProfileView.as_view(), name="Doctor-profile"),
    path('education/add', DoctorEducationView.as_view(), name="Doctor-education-add"),
] 

