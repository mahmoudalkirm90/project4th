from rest_framework import serializers
from .models import Doctor , Job_title , Education
from users.models import User , Otp
from users.serializers import UserDoctorSerializer
from django.db import transaction 
from users.mail_sender import send_email
from django.contrib.auth.hashers import make_password
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

class job_titleSerialzer(serializers.ModelSerializer):
    class Meta: 
        model = Job_title
        fields = "__all__"   
class UserUpdateSerialzer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['gender','birth_date','phone']

class DoctorProfileSerialzer(serializers.ModelSerializer):
    user = UserUpdateSerialzer()
    job_title = job_titleSerialzer()
    class Meta: 
        model = Doctor
        fields = ['user','job_title','experience','specialization']
    

    def update(self,instance,validated_data):
        user_data = validated_data.pop('user')

        user = instance.user
        job_title_data = validated_data.pop('job_title')

        instance.specialization = validated_data.get('specialization',instance.specialization)
        instance.experience = validated_data.get('experience', instance.experience) 
        instance.save()

        job_title_obj = Job_title.objects.get_or_create(job_title_data)
        user.job_title = job_title_obj

        user.gender = user_data.get('gender',user.gender)
        user.birth_date = user_data.get('birth_date',user.birth_date)
        user.phone = user_data.get('phone',user.phone)
        user.save()

        

        return instance

class DoctorEducationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Education
        # fields = ['degree','institution','graduation_year','license_number']
        fields = [
            'degree',
            'institution',
            'graduation_year',
            'license_number',
            'certificate'
        ]
        