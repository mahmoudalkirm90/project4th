from rest_framework import generics
from rest_framework import viewsets
from .serializers import PricesSerializer
from .models import SessionPrice
from rest_framework import permissions
from users.permissions import IsDoctor

class SessionPricesViewSet(viewsets.ModelViewSet):
    serializer_class = PricesSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    lookup_field = 'type'

    def get_queryset(self):
        return SessionPrice.objects.filter(doctor=self.request.user.doctor)

    # def get_object(self):
    #     print(self.kwargs.get('type'))
    #     print(self.kwargs.get('type'))
    #     print(self.kwargs.get('type'))
    #     return SessionPrice.objects.filter(type=self.kwargs.get('type'))
 
    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor)
