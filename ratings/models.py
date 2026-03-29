from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Rating(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating by {self.patient} for {self.doctor}: {self.rating}"