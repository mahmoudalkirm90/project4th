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
    title = serializers.CharField(required=False)
    class Meta: 
        model = Job_title
        fields = ["title",] 
class UserUpdateSerialzer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['gender','birth_date','phone']

class DoctorProfileSerialzer(serializers.ModelSerializer):
    user = UserUpdateSerialzer(required=False)
    job_title = job_titleSerialzer(required=False)
    class Meta: 
        model = Doctor
        fields = ['user','job_title','experience','specialization']
    

    def update(self,instance,validated_data): 
        user_data = validated_data.pop('user',None)
        user = instance.user
        job_title_data = validated_data.pop('job_title',None)

        with transaction.atomic():
            instance.specialization = validated_data.get('specialization',instance.specialization)
            instance.experience = validated_data.get('experience', instance.experience) 
            
            title = job_title_data.get('title') if job_title_data else None
            if title:
                job_title_obj, _ = Job_title.objects.get_or_create(title=title)
                instance.job_title = job_title_obj  
            
            instance.save()
    
            if user_data:
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
        