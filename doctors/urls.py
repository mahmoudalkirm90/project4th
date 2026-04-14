from django.urls import path
from .views import DoctorRegisterView , DoctorProfileView , DoctorEducationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile/education',DoctorEducationView,basename='doctor-education')
urlpatterns = [
    path('register/', DoctorRegisterView.as_view(), name='doctor-register'),
    path('profile/update', DoctorProfileView.as_view(), name="Doctor-profile"),
]

urlpatterns += router.urls
