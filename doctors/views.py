from django.shortcuts import render
from rest_framework import generics
from .models import Doctor, Education
from .serializers import DoctorRegisterSerializer , DoctorProfileSerialzer , DoctorEducationSerializer
from rest_framework.response import Response 
from users.permissions import IsDoctor , IsVerified 
from rest_framework import permissions, viewsets


class DoctorRegisterView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegisterSerializer
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Doctor registered successfully"
                          , "is_verified":False},
                           status=201)
    
class DoctorProfileView(generics.UpdateAPIView):

    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerialzer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.doctor
        
    def update(self, request, *args, **kwargs):
        res =super().update(request, *args, **kwargs)
        return Response({
            "data":res.data,
            "message": "Doctor profile updated successfully"}, status=200)
    
class DoctorEducationView(generics.CreateAPIView):
    serializer_class = DoctorEducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Education.objects.filter(
            doctor = self.request.user.doctor
        )
    def create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(doctor=self.request.user.doctor)
        return Response({
            "message": "Doctor education added successfully"
        }, status=201)

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Education.objects.get(id=pk, doctor=self.request.user.doctor)