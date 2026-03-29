from django.db import models
from django.utils import timezone
from users.models import User
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    class Status (models.TextChoices):
        Pending = 'pending' , 'Pending' 
        Confirmed = 'confirmed' , 'Confirmed'
        Cancelled = 'cancelled' , 'Cancelled'
        
    class Type(models.TextChoices):
        Video = 'video' , 'Video'
        Audio = 'audio' , 'Audio'
        TextMessage = 'text_message' , 'Text Message'

    appointment_type = models.CharField(max_length=100 , choices=Type.choices , default=Type.TextMessage)
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField() # in minutes
    status = models.CharField(max_length=100 , choices= Status.choices , default=Status.Pending)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class SessionPrice(models.Model):
    Doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='session_prices',
    )
    class Type(models.TextChoices):
        Video = 'video' , 'Video'
        Audio = 'audio' , 'Audio'
        TextMessage = 'text_message' , 'Text Message'
    duration = models.IntegerField() # in minutes
    type = models.CharField(max_length=100 , choices= Type.choices)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
# create the perscription then add the medications to it in the same request 
class Prescription(models.Model):
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment , on_delete=models.CASCADE , blank=True)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True , null=True)
    # يمكن أن يكون هناك أكثر من دواء في نفس الوصفة الطبية

class Medication(models.Model):
    prescription = models.ForeignKey(Prescription , on_delete=models.CASCADE , related_name='medications')

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True , null=True)
    side_effects = models.TextField(blank=True , null=True)

    # Usage instructions (optional)
    dosage_amount = models.IntegerField(blank=True , null=True)
    dosage_duration = models.IntegerField(blank=True , null=True) # in days
    dosage_interval = models.IntegerField(blank=True , null=True) # in hours

    def __str__(self):
        return self.name

class Payment(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='payment'
        )
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100 , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)