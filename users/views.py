from matplotlib.pylab import rand
from rest_framework.decorators import api_view
from users.models import Otp
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer
from django.utils import timezone
from .models import User
from .mail_sender import send_email 

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

@api_view(['POST'])
def resend_otp(request):
    email = request.data.get('email')
    otps = Otp.objects.filter(user__email=email, is_used=False).order_by('-created_at')
    for otp in otps:
        if otp.expires_at > timezone.now():
            send_email(receiver_email=otp.user.email, otp_code=otp.code)  # Resend the existing OTP
            return Response({"message": "OTP resent successfully"}, status=200)
    # If no valid OTP exists, create
        
    user = User.objects.filter(email=email).first()
    if user:
        if user.is_verified:
            return Response({"message": "User is already verified"}, status=400)
        new_otp = Otp.objects.create(user=user, code=Otp.generate_otp())
        send_email(email, new_otp.code)  # Send the new OTP
        return Response({"message": "New OTP generated and sent successfully"}, status=200)
    return Response({"message": "User with this email does not exist"}, status=400)
    