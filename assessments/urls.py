from django.urls import path
from .views import ServeyFormView , SubmitAnswerView

urlpatterns = [
    path('form/', ServeyFormView.as_view(), name='servey-form'),
    path('form/submit/', SubmitAnswerView.as_view(), name='submit-answer')
]