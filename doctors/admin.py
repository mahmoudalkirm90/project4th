from django.contrib import admin
from .models import Doctor , DoctorSchedule, DoctorEducation , DoctorPaymentMethod ,    DoctorSpecialties , MainSpecialization
# Register your models here.

Models = [
    Doctor,
    DoctorSchedule,
    DoctorEducation,
    DoctorPaymentMethod,
    DoctorSpecialties,
    MainSpecialization,
]

admin.site.register(Models)