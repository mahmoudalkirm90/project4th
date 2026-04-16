from matplotlib.pylab import rand
from rest_framework.decorators import api_view
from users.models import Otp
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ( UserLoginSerializer,
                           ResendOtpSerializer,
                           VerifyOtpSerializer)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    # permission_classes = [IsVerified,]
    def post(self, request, *args, **kwargs):   
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=200)

# expected json data for request : 
# {
#     "code": "123456",
#     "email": "example@afiete.com"
# }
class ResendOtpView(generics.GenericAPIView):
    serializer_class = ResendOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=200)

class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=200)