from django.contrib import admin
from .models import Doctor , Education , PaymentMethod, Schedule, Specialties, job_title
# Register your models here.

Models = [
    Doctor,
    Schedule,
    Education,
    PaymentMethod,
    Specialties,
    job_title,
]

admin.site.register(Models)