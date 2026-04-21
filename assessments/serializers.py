from rest_framework import serializers
from .models import QuestionGroup, Question, AnswerOption, UserAnswer
from rest_framework.response import Response
from django.db import transaction
class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question  
        fields = ['id', 'text', 'order', 'options']
    

class ServeyFormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = QuestionGroup
        fields = ['id', 'name', 'description', 'order', 'questions']

class UserAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()

class SubmitAnswerSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True)

    class Meta: 
        model = UserAnswer
        fields = ['answers']
    def create(self, validated_data):
        request = self.context['request']
        patient = request.user.patient

        answers_data = validated_data.get('answers', [])
        objects = []
        for item in answers_data:
            question_id = item.get('question_id')
            answer_id = item.get('answer_id')

            question = Question.objects.get(id=question_id)
            answer_option = AnswerOption.objects.get(id=answer_id)

            if answer_option.question_id != question_id:
                raise serializers.ValidationError(
                    f"Answer option {answer_id} does not belong to question {question_id}."
                )
            # if UserAnswer.objects.filter(patient=patient, question_id=question_id).first():
            #     raise serializers.ValidationError(
            #         f"Answer for question {question_id} already exists"
            #     )
            objects.append(UserAnswer(patient=patient, question=question, answer_option=answer_option))
        try:
            with transaction.atomic():
                UserAnswer.objects.bulk_create(objects)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return request.data


"""
{
    "answers": [{
           "question_id":1,
           "answer_id":2}
]
}

"""