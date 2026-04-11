from rest_framework import serializers
from .models import Doctor , job_title , Specialties , Education
from users.models import User , Otp
from users.serializers import UserDoctorSerializer
from django.db import transaction 
from users.mail_sender import send_email
from django.contrib.auth.hashers import make_password
import uuid
class DoctorRegisterSerializer(serializers.ModelSerializer):
    user = UserDoctorSerializer()
    class Meta:
        model = Doctor
        fields = ['user',]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        try:
            with transaction.atomic():
                user_serializer = UserDoctorSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
                doctor = Doctor.objects.create(user=user, **validated_data)
                code = Otp.generate_otp()
                hash_code = make_password(code)
                Otp.objects.create(user=user, code=hash_code)    
                transaction.on_commit(lambda: send_email(
                    receiver_email=user.email,
                    otp_code=code,
                ))
            
            return doctor
        except Exception as e:
            raise serializers.ValidationError(str(e)) 