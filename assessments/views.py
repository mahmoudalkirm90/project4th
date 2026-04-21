from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import generics

from assessments.models import QuestionGroup , UserAnswer
from .serializers import ServeyFormSerializer, UserAnswerSerializer , SubmitAnswerSerializer

class ServeyFormView(generics.ListAPIView):
    serializer_class = ServeyFormSerializer
    queryset = QuestionGroup.objects.prefetch_related('questions__options').all()  

class SubmitAnswerView(generics.CreateAPIView):
    serializer_class = SubmitAnswerSerializer 
    queryset = UserAnswer.objects.all() 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Answer saved successfully."},
            status=200
        )
    