from matplotlib.pylab import rand
from rest_framework.decorators import api_view
from users.models import Otp
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UserLoginSerializer,
                           ResendOtpSerializer,
                           VerifyOtpSerializer)
from django.utils import timezone
from .models import User
from .mail_sender import send_email 

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    # permission_classes = [IsVerified,]
    def post(self, request, *args, **kwargs):   
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)

# expected json data for request : 
# {
#     "code": "123456",
#     "email": "example@afiete.com"
# }

@api_view(['POST'])
def verify_otp(request):
    code = request.data.get('code')
    email = request.data.get('email')
    otps = Otp.objects.filter(is_used=False, expires_at__gt=timezone.now()).order_by('-created_at')
    for otp in otps:
         if check_password(code, otp.code):
            otp.is_used = True
            otp.save()
            user = otp.user
            user.is_verified = True
            user.save()
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response({"message": "OTP verified successfully"
                             ,"refresh": str(refresh),
                               "access": str(refresh.access_token)},
                              status=200)
    
    return Response({"message": "Invalid OTP or email"}, status=400)

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