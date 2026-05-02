from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Otp
from .serializers import ( UserLoginSerializer,
                           ResendOtpSerializer,
                           VerifyOtpSerializer,
                           DeleteAccountSerializer,
                           PasswordResetSerializer,
                           EmailResetSerializer,
                           UserInfoSerializer,
                           ForgetPasswordVerifyOtpSerializer,
                           ForgetPasswordSerializer,
                           ResetPasswordSerializer
                           )
from doctors.serializers import DoctorProfileSerialzer
from patients.serializers import PatientProfileSerializer
from .mail_sender import send_email
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
import threading


from .utils import *
class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_data = UserInfoSerializer(user).data
        refresh = RefreshToken.for_user(user)
        
        role = "doctor" if is_doctor(user) else "patient" if is_patient(user) else "Anonymous"
        details = ""
        if role == "doctor":
            details = DoctorProfileSerialzer(user.doctor).data
        elif role == "patient":
            details = PatientProfileSerializer(user.patient).data
        return Response({"message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": str(role),
                "user":user_data,
                str(role): details
                }, status=200)

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
        refresh = RefreshToken.for_user(self.request.user)

        return Response(
             {      "is_verified":True,
                    "message": "OTP verified successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token) 
             },
             status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)   
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):

    permission_classes = [IsAuthenticated] 
    # allowed_methods = ['DELETE',"POST"]
    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)

class PasswordResetView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer

    def get_object(self):
        return self.request.user
    def update(self,request):
        serializer = self.get_serializer(self.get_object(),data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Password reseted successfully",
        },status=status.HTTP_200_OK)

class EmailResetView(generics.UpdateAPIView):
    queryset = User.objects.all()   
    permission_classes = [IsAuthenticated]
    serializer_class = EmailResetSerializer
    def update(self,request):
        serializer = self.get_serializer(self.get_object(),data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message":"Email reseted successfully, please verify your new email",
         },status=status.HTTP_200_OK) 
        
    def get_object(self):
        return self.request.user

class ForgotPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        user = self.request.user


        code = Otp.generate_otp()
        hashed_code = make_password(code)
        Otp.objects.create(user=user, code=hashed_code)

        threading.Thread(target=send_email, args=(user.email, code)).start()

        return Response(
            {"message": "OTP sent to your email"},
            status=status.HTTP_200_OK
        )


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = ForgetPasswordVerifyOtpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "OTP verified successfully"
             , "can_reset_password":True
             , "is_verified":True},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK
        )