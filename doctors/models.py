from django.db import models
from users.models import User
# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    
    specialization = models.CharField(max_length=100 , blank=True , null=True)
    bio = models.TextField(blank=True , null=True)
    experience = models.IntegerField(blank=True , null=True)
    rating = models.FloatField(blank=True , null=True)

class DoctorDomain(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='domains')
    domain = models.CharField(max_length=100)

# اوقات الدوام للأطباء
class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='schedules')
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    day_of_week = models.CharField(max_length=20, choices=DAYS_OF_WEEK) # e.g., Monday, Tuesday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    # يمكن أن يكون هناك أكثر من توقيت في نفس اليوم لنفس الطبيب
