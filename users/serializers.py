from rest_framework import serializers
from users.models import User
from users.models import Otp
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import is_doctor , is_patient
from .mail_sender import send_email
from django.utils import timezone
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError("Patient with this email does not exist.")
            
        if user.check_password(attrs['password']):
            raise serializers.ValidationError("Incorrect password.")
        if not user.is_verified:
            raise serializers.ValidationError("Account is not verified. Please verify your account before logging in.")
        user_serializer = UserSerializer(user,many=False)
        refresh = RefreshToken.for_user(user)
        
        return {"message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user":user_serializer.data,
                "role": "doctor" if is_doctor(user) else "patient" if is_patient(user) else "Anonymous"
                }

class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        email = self.validated_data['email']

        # البحث عن OTP صالح
        otp = Otp.objects.filter(
            user__email=email,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()

        if otp:
            send_email(
                receiver_email=otp.user.email,
                otp_code=otp.code
            )
            return {"message": "OTP resent successfully"}

        # إنشاء OTP جديد
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist"}
            )

        if user.is_verified:
            raise serializers.ValidationError(
                {"email": "User is already verified"}
            )

        new_otp = Otp.objects.create(
            user=user,
            code=Otp.generate_otp()
        )

        send_email(user.email, new_otp.code)

        return {"message": "New OTP generated and sent successfully"}

from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def create(self, validated_data):
        email = validated_data['email']
        code = validated_data['code']

        otps = Otp.objects.filter(
            user__email=email,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at')

        for otp in otps:
            if check_password(code, otp.code):
                otp.is_used = True
                otp.save()

                user = otp.user
                user.is_verified = True
                user.save()

                refresh = RefreshToken.for_user(user)

                return {
                    "message": "OTP verified successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }

        raise serializers.ValidationError({
            "detail": "Invalid OTP or email"
        })