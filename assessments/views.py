from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import generics
from rest_framework.views import APIView
from assessments.models import QuestionGroup , UserAnswer
from .serializers import ServeyFormSerializer, UserAnswerSerializer , SubmitAnswerSerializer, ScoresSerializer
from .recommender import recommend_doctors
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

# questionnaire/views.py

class PatientScoresView(APIView):

    def get(self, request):
        scores = ScoresSerializer(request.user.patient).data
        return Response(scores)

# doctors/views.py

class RecommendDoctorsView(APIView):

    def get(self, request):
        patient     = request.user.patient
        recommended = recommend_doctors(patient)

        return Response({"recommended_doctors": recommended})