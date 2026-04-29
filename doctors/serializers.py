from rest_framework import serializers
from .models import (Doctor,
                     Job_title,
                     Education,
                     Schedule,
                     SubSpecialization)
from users.models import User , Otp
from users.serializers import UserDoctorSerializer
from django.db import transaction 
from users.mail_sender import send_email
from threading import Thread
from django.contrib.auth.hashers import make_password
from django.db.models import Q

class DoctorRegisterSerializer(serializers.ModelSerializer):
    user = UserDoctorSerializer()
    class Meta:
        model = Doctor
        fields = ['user',]
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        with transaction.atomic():
            user_serializer = UserDoctorSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            doctor = Doctor.objects.create(user=user, **validated_data)
            code = Otp.generate_otp()
            hash_code = make_password(code)
            Otp.objects.create(user=user, code=hash_code)    
        Thread(target=send_email, args=(user.email, code)).start()
        
        return doctor

class job_titleSerialzer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    class Meta: 
        model = Job_title
        fields = ["title",] 
class UserUpdateSerialzer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['gender','birth_date','phone']
class SubSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSpecialization
        fields = "__all__"
        
class DoctorProfileSerialzer(serializers.ModelSerializer):
    user = UserUpdateSerialzer(required=False)
    job_title = job_titleSerialzer(required=False)
    specialties = SubSpecializationSerializer(required=False,many=True)
    class Meta: 
        model = Doctor
        fields = ['user','job_title','specialties','experience']
    

    def update(self,instance,validated_data): 
        user_data = validated_data.pop('user',None)
        user = instance.user
        job_title_data = validated_data.pop('job_title',None)
        specialties_data = validated_data.pop('specialties',None)

        with transaction.atomic():
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
            if specialties_data:
                subs = []
                for obj in specialties_data:
                    sub, _ = SubSpecialization.objects.get_or_create(name=obj.get('name'))
                    subs.append(sub)
                
                instance.specialties.set(subs)
        

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

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Schedule
        fields = ['id','day_of_week','start_time','end_time']
        
    
    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")
        
        return attrs


    def update(self, instance, validated_data):
        doctor = instance.doctor
        view = self.context.get('view')
        id = view.kwargs.get(view.lookup_field)

        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')

        day_of_week = validated_data.get("day_of_week")
        schedule = Schedule.objects.get(doctor=doctor, day_of_week=day_of_week, id=id)
        if not schedule: 
            raise serializers.ValidationError("Schedule not found for the specified day.")

        # تم استثناء العنصر من القاىمة لمنع التضارب

        anotherSchedules = Schedule.objects.filter(~Q(id=schedule.id), doctor=doctor, day_of_week=day_of_week)
        for obj in anotherSchedules: 
            print(obj.id)
            if start_time < obj.end_time and end_time > obj.start_time:
                raise serializers.ValidationError(f'This is Overlaps with {day_of_week} schedule')
            

        schedule.start_time = start_time
        schedule.end_time = end_time
        schedule.save()

        return validated_data

    def create(self, validated_data):
        doctor = self.context['request'].user.doctor
        day_of_week = validated_data.get('day_of_week')
        
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')

        anotherSchedules = Schedule.objects.filter(doctor=doctor, day_of_week=day_of_week)
        for obj in anotherSchedules: 
            if start_time < obj.end_time and end_time > obj.start_time:
                raise serializers.ValidationError(f'This is Overlaps with {day_of_week} schedule')

                    

        schedule = Schedule.objects.create(doctor=doctor, day_of_week=day_of_week , start_time=start_time, end_time=end_time)
        
        schedule.save()

        return validated_data