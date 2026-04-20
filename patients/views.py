from .models import *
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PatientRegisterSerializer , PatientProfileSerializer
from rest_framework import permissions
from users.permissions import IsPatient

class PatientRegisterView(generics.CreateAPIView):
    serializer_class = PatientRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Patient registered successfully"
                          , "is_verified":False},
                           status=201)

class PatientProfileView(generics.UpdateAPIView):
    serializer_class = PatientProfileSerializer
    queryset = Patient.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsPatient]  # Add appropriate permissions here 

    def get_object(self):
        return self.request.user.patient