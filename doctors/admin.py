from django.contrib import admin
from .models import Doctor , DoctorDomain , DoctorSchedule
# Register your models here.

Models = [
    Doctor,
    DoctorDomain,
    DoctorSchedule,
]

admin.site.register(Models)