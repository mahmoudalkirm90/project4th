from django.contrib import admin
from .models import *

Models = [
    Appointment,
    Prescription,   
    Medication,
]

admin.site.register(Models)