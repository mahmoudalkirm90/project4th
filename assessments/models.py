from django.db import models
from patients.models import Patient

# Question groupe 
# |
# Question 
# |
# AnswerOptions
# |
# UserAnswer

class QuestionGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    text = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='answers')
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE , null=False , default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient} - {self.question}: {self.answer_option}"