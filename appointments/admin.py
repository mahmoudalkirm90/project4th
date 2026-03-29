from django.contrib import admin
from .models import *

Models = [
    Appointment,
    Prescription,   
    Medication,
    SessionPrice,
    Payment,
]

admin.site.register(Models)