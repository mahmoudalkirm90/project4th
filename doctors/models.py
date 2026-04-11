from django.db import models
from users.models import User
# Create your models here.

class job_title(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
class Doctor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    job_title = models.ForeignKey(job_title, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True , null=True)
    experience = models.IntegerField(blank=True , null=True)
    specialization = models.CharField(max_length=100 , blank=True , null=True) # the main specialization of the doctor
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # to track the approval status of the doctor
    
    def __str__(self):
        return self.user.username
    
    @property 
    def specialization_list(self):
        return 

# for the doctor to add more specializations if he has more than one
class Specialties(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='specializations')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.doctor.user.username} - {self.name}"

class Education(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='educations')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    graduation_year = models.PositiveIntegerField(blank=True , null=True)
    license_number = models.CharField(max_length=100 , blank=True , null=True)
    brief_description = models.TextField(blank=True , null=True)
    
    certificate = models.FileField(upload_to=f'media/certificates/%Y/%m/%d/', blank=True , null=True) # to allow doctors to upload their certificates or licenses
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # to track the approval status of the education record
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # to track when the education record
   
    reveiwed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='education_reviews') # to track which admin reviewed the education record
    reveiwed_at = models.DateTimeField(blank=True , null=True) # to track when the education record was reviewed7
    reveiwer_comment = models.TextField(blank=True , null=True) # to allow the admin to add comments when reviewing the education record
    def __str__(self):
        return f"{self.doctor.user.username} - {self.degree}"

# اوقات الدوام للأطباء
class Schedule(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # to track when the schedule was last updated
    # يمكن أن يكون هناك أكثر من توقيت في نفس اليوم لنفس الطبيب

class PaymentMethod(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='payment_methods')
    method = models.CharField(max_length=100) # e.g., Credit Card, PayPal, etc.

    is_active = models.BooleanField(default=True) # to allow doctors to activate or deactivate payment methods without deleting them
    details = models.TextField(blank=True , null=True) # to store any additional details related to the payment method (e.g., account number, etc.)