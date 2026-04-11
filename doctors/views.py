from django.shortcuts import render
from rest_framework import generics
from .models import Doctor
from .serializers import DoctorRegisterSerializer
from rest_framework.response import Response

class DoctorRegisterView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegisterSerializer
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Doctor registered successfully"
                          , "is_verified":False},
                           status=201)