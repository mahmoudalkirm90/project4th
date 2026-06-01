from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Article, Reaction
from doctors.models import SubSpecialization, Doctor
from users.models import User 
from doctors.serializers import job_titleSerialzer
class AuthorDoctorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = ['username','first_name', 'last_name']

class AuthorSerializer(serializers.ModelSerializer):
    user = AuthorDoctorSerializer()
    job_title = job_titleSerialzer()
    class Meta: 
        model = Doctor
        fields = ['user','job_title','photo'] 
class ArticaleCraeteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Article
        fields = [
            "title",
            "content",
            "specialization",
        ]
    
    def validate_specialization(self, value):
        doctor = self.context['request'].user.doctor
        if value.name not in doctor.specialization_list:
            raise ValidationError('specialization not related to the doctor')
        return value
    def create(self, validated_data):
        doctor = self.context['request'].user.doctor
        Article.objects.create(author=doctor,status='Pending',**validated_data)
        return validated_data

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSpecialization
        fields = ['name']
class ArticleRetrieveSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer(read_only=True)
    author = AuthorSerializer()
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    class Meta: 
        model = Article
        fields = "__all__"

class ArticlesMostReactionScoreSerializer(serializers.ModelSerializer): 
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    author = AuthorSerializer()
    specialization = SpecializationSerializer(read_only=True)

    class Meta: 
        model = Article
        fields = "__all__"

class ReactionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Reaction
        fields = ["reaction"]

class DeleteArticleSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Article
        fields = []

class ArticleSerializer(serializers.ModelSerializer): 
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    author = AuthorSerializer()
    specialization = SpecializationSerializer(read_only=True)

    class Meta:     
        model = Article
        fields = "__all__"