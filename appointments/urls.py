from rest_framework.routers import DefaultRouter
from .views import (BookAppointmentView,
                    PatientAppointmentListView,
                    DoctorAppointmentListView,
                    ConfirmAppointmentView,
                    CancelAppointmentView,
                    RetrieveAppointmentAPIView)
from django.urls import path
urlpatterns = [
    path('', BookAppointmentView.as_view(), name='book-appointment'),
    path('my-appointments/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('doctor-dashboard/', DoctorAppointmentListView.as_view(), name='doctor-appointments'),

    path('<int:pk>/confirm/', ConfirmAppointmentView.as_view(), name='confirm-appointment'),
    path('<int:pk>/cancel/', CancelAppointmentView.as_view(), name='cancel-appointment'),

    path('<int:pk>', RetrieveAppointmentAPIView.as_view(), name='retrieve')

]