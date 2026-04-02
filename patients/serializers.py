from rest_framework import serializers
from django.db import transaction
from .models import Patient
from random import randint
from users.models import User
from users.models import Otp
from users.mail_sender import send_email
from users.serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from users.serializers import UserSerializer

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['user', 'code', 'is_used', 'created_at']
    
    
class PatientRegisterSerializer(serializers.ModelSerializer):
        user = UserSerializer()
        class Meta:
            model = Patient
            fields = ['user', 'psychological_history']
        def create(self, validated_data):
            otp_code = str(randint(100000, 999999))
            hashed_otp_code = make_password(otp_code)
            with transaction.atomic():
                user_data = validated_data.pop('user')
                user = User.objects.create_user(**user_data)
                patient = Patient.objects.create(user=user, **validated_data)
                Otp.objects.create(user=user, code=hashed_otp_code)
            send_email(
            smtp_server="smtp.gmail.com",
            port=587,
            sender_email="afiete2026@gmail.com",
            sender_password="nmmsuchwtfunhwhy", # eco password not real for security
            receiver_email=f'{user.email}',
            subject="Welcome to Afiete",
            body=f"""Hello,

I hope you are doing well.

I would like to request a One-Time Password {otp_code} to complete my account verification process.
Please send the OTP to this email address or provide guidance on how I can receive it.

Thank you for your assistance.

Best regards,
Afiete Team""",
            )
            return patient


