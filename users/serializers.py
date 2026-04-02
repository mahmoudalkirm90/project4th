from rest_framework import serializers
from users.models import User
from users.models import Otp
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import is_doctor , is_patient

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
