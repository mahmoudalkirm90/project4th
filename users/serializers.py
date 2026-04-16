from rest_framework import serializers
from users.models import User
from users.models import Otp
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import is_doctor , is_patient
from .mail_sender import send_email
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import uuid
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}

class UserDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        first_name = (validated_data.get('first_name') or '').strip()
        last_name = (validated_data.get('last_name') or '').strip()
    
        username = f"{first_name or 'user'}_{last_name or 'doc'}_{str(uuid.uuid4())[:8]}".lower()
        user = User.objects.create_user(
            username=username,
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=first_name,
            last_name=last_name
        )
    
        return user 
    
class UserLoginSerializer(serializers.Serializer):  
    email = serializers.EmailField()
    password = serializers.CharField() 

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError("Patient with this email does not exist.")
            
        if not user.check_password(attrs['password']):
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
        Otp.objects.filter(user=user, is_used=False).update(is_used=True)
        code = Otp.generate_otp()
        hashed_code = make_password(code)
        new_otp = Otp.objects.create(
            user=user,
            code= hashed_code
        )

        send_email(user.email, code)

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