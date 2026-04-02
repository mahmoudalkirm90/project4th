from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PatientRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class PatientRegisterView(generics.CreateAPIView):
    serializer_class = PatientRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Patient registered successfully"
                          , "is_verified":False},
                           status=201)

