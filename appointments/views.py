from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import (PricesSerializer,
                          AppointmentSerializer,
                          AppointmentListSerializer,
                          RetrieveAppointmentSerializer,)
from .models import SessionPrice, Appointment
from users.permissions import IsDoctor, IsPatient

from django.shortcuts import get_object_or_404
class SessionPricesViewSet(viewsets.ModelViewSet):
    serializer_class = PricesSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    lookup_field = 'type'

    def get_queryset(self):
        return SessionPrice.objects.filter(doctor=self.request.user.doctor)

 
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor)


class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save() # 
            return Response({
                "message":"“Your reservation request has been submitted successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientAppointmentListView(ListAPIView):
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.patient).order_by('-date')

class DoctorAppointmentListView(ListAPIView):
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user.doctor).order_by('-date')
        
# خاص بالطبيب
class ConfirmAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request, pk):
        appointment = get_object_or_404(
            Appointment, 
            pk=pk, 
            doctor=request.user.doctor, 
            status=Appointment.Status.Pending
        )
        
        appointment.status = Appointment.Status.Confirmed
        appointment.save()
        
        return Response({"message": "The appointment has been confirmed successfully."}, status=status.HTTP_200_OK)

class CancelAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        appointment = get_object_or_404(
            Appointment, 
            pk=pk, 
            status=Appointment.Status.Pending
        )
        
        # السماح للطبيب أو المريض بإلغاء الموعد
        if appointment.doctor.user != request.user and appointment.patient.user != request.user:
            return Response({"error": "You do not have the authority to cancel this appointment"}, status=status.HTTP_403_FORBIDDEN)
        
        appointment.status = Appointment.Status.Cancelled
        appointment.save()
        
        return Response({"message": "The appointment has been successfully cancelled."}, status=status.HTTP_200_OK)

class RetrieveAppointmentAPIView(RetrieveAPIView): 
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = RetrieveAppointmentSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Appointment.objects.filter(
            doctor = self.request.user.doctor
        )