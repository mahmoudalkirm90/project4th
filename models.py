from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta, date
# User -> patiant 
# User -> doctor 
# User -> Admin


class User(AbstractUser):
    
    class Gender (models.TextChoices):
        Male = 'male' , 'Male'
        Female = 'female' , 'Female'
    class Status (models.TextChoices):
        Active = 'active' , 'Active'
        Deactive = 'deactive' , 'Deactive'
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15 , blank=True , null=True)
    birth_date = models.DateField(blank=True , null=True)

    gender = models.CharField(max_length=100 , choices=  Gender.choices , null= True , blank=True)
    status = models.CharField(max_length=100 , choices= Status.choices , default=Status.Active)
    
    is_verified =   models.BooleanField(default=False) # to check if the user has verified his email or not
    # otp_code = models.CharField(max_length=6 , blank=True , null=True) # to store the OTP code for email verification
    can_reset_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()
        if self.birth_date: 
            return today.year - self.birth_date.year - ((today.month, today.day) < 
                                                        (self.birth_date.month, self.birth_date.day) )
        return None
class notes(models.Model):
    Author = models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def otp_expiry():
    return timezone.now() + timedelta(minutes=10)
class Otp(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    code = models.CharField(max_length=120)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=otp_expiry) # OTP expires after 10 minutes

    def generate_otp():
        from random import randint
        return str(randint(1000, 9999))
    
class Report(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Rating(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, default=None, null=True)
    rating = models.PositiveIntegerField()
    comment = models.CharField(max_length=255, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
class Patient(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100 , blank=True , null=True)
    psychological_history = models.TextField(blank=True , null=True)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}'

from django.db import models
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class FeelingType(models.TextChoices):
    HAPPY = 'happy', 'Happy'
    SAD = 'sad', 'Sad'
    ANGRY = 'angry', 'Angry'
    NEUTRAL = 'neutral', 'Neutral'
    ANXIOUS = 'anxious', 'Anxious'

class MusicTherapeuticGoal(models.TextChoices):
    CALM_DOWN = 'calmDown', 'Calm Down'
    UPLIFT = 'uplift', 'Uplift'
    STABILIZE = 'stabilize', 'Stabilize'
    FOCUS = 'focus', 'Focus'
    SLEEP = 'sleep', 'Sleep'

class MusicSourceType(models.TextChoices):
    BENSOUND = 'bensound', 'Bensound'
    FREEMUSICARCHIVE = 'freemusicarchive', 'Free Music Archive'
    PIXABAY = 'pixabay', 'Pixabay'
    INCOMPETECH = 'incompetech', 'Incompetech'
    CUSTOM = 'custom', 'Custom'

class BreathingExerciseType(models.TextChoices):
    BOX_BREATHING = 'boxBreathing', 'Box Breathing'
    FOUR_SEVEN_EIGHT = 'fourSevenEight', '4-7-8 Breathing'
    DIAPHRAGMATIC = 'diaphragmatic', 'Diaphragmatic Breathing'
    PACED_BREATHING = 'pacedBreathing', 'Paced Breathing'
    RESONANCE = 'resonance', 'Resonance Breathing'


class MusicEntity(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    audio_url = models.URLField()
    preview_url = models.URLField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)
    source_name = models.CharField(max_length=100)
    source_url = models.URLField()
    source_type = models.CharField(max_length=50, choices=MusicSourceType.choices, default=MusicSourceType.CUSTOM)
    
    # Storing lists as JSON for clean architecture mapping
    supported_feelings = models.JSONField(help_text="List of FeelingType strings")
    therapeutic_goals = models.JSONField(help_text="List of MusicTherapeuticGoal strings")
    
    is_instrumental = models.BooleanField(default=True)
    duration_seconds = models.IntegerField()
    tempo_bpm = models.IntegerField()
    novelty_score = models.IntegerField(default=5)
    license_text = models.TextField()
    attribution_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"


class BreathingExerciseEntity(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=BreathingExerciseType.choices)
    duration_minutes = models.IntegerField()
    inhale_seconds = models.IntegerField()
    hold_seconds = models.IntegerField()
    exhale_seconds = models.IntegerField()
    rest_seconds = models.IntegerField()
    steps = models.JSONField(help_text="Ordered list of string steps")
    recommended_for = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class UserRelaxProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='relax_profile')
    last_selected_feeling = models.CharField(max_length=20, choices=FeelingType.choices, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Relax Profile for {self.user.username}"
    

class Job_title(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SubSpecialization(models.Model):
    name           = models.CharField(max_length=255, default='')  # ← مو blank/null
    question_group = models.ForeignKey(
        QuestionGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subspecializations'
        , default=None
    )
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    job_title = models.ForeignKey(Job_title, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True , null=True)
    experience = models.IntegerField(blank=True , null=True)
    
    STATUS_CHOICES = [ 
        ('pending', 'Pending'),
        ('approved', 'Approved'), 
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') # to track the approval status of the doctor
    photo = models.ImageField(upload_to='media/doctor_photos/%Y/%m/%d/', blank=True , null=True) # to allow doctors to upload their photos
    specialties = models.ManyToManyField(SubSpecialization)
    def __str__(self):
        return self.user.username
    
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
    
    def __str__(self):
        return f"{self.doctor.user.username} - {self.day_of_week} ({self.start_time} - {self.end_time})"
class PaymentMethod(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='payment_methods')
    method = models.CharField(max_length=100) # e.g., Credit Card, PayPal, etc.

    is_active = models.BooleanField(default=True) # to allow doctors to activate or deactivate payment methods without deleting them
    details = models.TextField(blank=True , null=True) # to store any additional details related to the payment method (e.g., account number, etc.)



class QuestionGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.order is None:
            last_order = QuestionGroup.objects.aggregate(
                models.Max('order')
            )['order__max']
            self.order = (last_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    questiongroup = models.ForeignKey(
        QuestionGroup,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.TextField()
    order = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.order is None:
            last_order = Question.objects.filter(
                questiongroup=self.questiongroup
            ).aggregate(models.Max('order'))['order__max']

            self.order = (last_order or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options'
    )
    text = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['patient', 'question']

    def clean(self):
        if self.answer_option.question_id != self.question_id:
            raise ValueError("Answer does not belong to the question")

    def __str__(self):
        return f"{self.patient} - {self.question}: {self.answer_option}"



class Article(models.Model):
    STATUS_CHOISES = [
        ("Pending","pending"),
        ("Approved","approved"),
        ("Rejected","rejected")
    ]
    objects = ArticleManager()
    author = models.ForeignKey(
        Doctor,
        on_delete= models.SET_NULL,
        null=True,
        blank=True
    )
    # status 
    status = models.CharField(max_length=15,choices=STATUS_CHOISES,default='pending')
    
    # content
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=5000)

    # dates
    created_at = models.DateTimeField(auto_now=True)

    # specialization related this article
    specialization = models.ForeignKey(
        SubSpecialization,
        null= True,
        blank=True,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.title} by {self.author.user.username}"
class Reaction(models.Model):
    LIKE    = 'like'
    DISLIKE = 'dislike'

    REACTION_CHOICES = [
        (LIKE,    'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    
   
    class Meta: 
        unique_together = ['article', 'user']  # كل يوزر يقدر يعمل reaction واحد بس
    
    def __str__(self):
        return f"{self.user} - {self.reaction} - {self.article}"

class Appointment(models.Model):
    class Status (models.TextChoices):
        Pending = 'pending'      # تم الحجز، بانتظار الدفع
        Confirmed = 'confirmed'  # تم الدفع
        Cancelled = 'cancelled'  # ملغي
        Completed = 'completed'  # انتهى الموعد
        Expired = 'expired'      # انتهى وقته بدون دفع
        
    class Type(models.TextChoices):
        Video = 'video' , 'Video'
        Audio = 'audio' , 'Audio'
        TextMessage = 'text_message' , 'Text Message'

    type = models.CharField(max_length=100 , choices=Type.choices , default=Type.TextMessage)
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.IntegerField() # in minutes
    status = models.CharField(max_length=100 , choices= Status.choices , default=Status.Pending)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_by = models.CharField(null=True, blank=True, max_length=20)
    def __str__(self):
        return f"Appointment between {self.patient} and {self.doctor} on {self.date} and id = {self.pk}"
    
    @property
    def end_time(self):
        return self.date + timezone.timedelta(minutes=self.duration)


class SessionPrice(models.Model):
    doctor = models.ForeignKey(
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
    class Status(models.TextChoices):
        Pending = 'pending', 'Pending'
        Completed = 'completed', 'Completed'
        Rejected = 'rejected', 'Rejected'
        Refunded = 'refunded', 'Refunded'
        
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='payment'
        )
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=100)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.Pending)
    transaction_id = models.CharField(max_length=100 , blank=True , null=True)
    viewed_by = models.ManyToManyField(User, blank=True, related_name='viewed_payments')

    created_at = models.DateTimeField(auto_now_add=True)