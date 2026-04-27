from rest_framework import serializers
from .models import *
from doctors.models import Doctor
from rest_framework.validators import ValidationError
class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPrice
        fields = ['duration','type','price']
    def validate_prive(self, value):
        if value < 0:
            raise ValidationError('invalid price')
    def create(self, validated_data):
        duration = validated_data.get('duration')
        type = validated_data.get('type')
        price = validated_data.get('price')

        doctor = self.context['request'].user.doctor

        if SessionPrice.objects.filter(type=type).exists():
            raise ValidationError(f'Session type {type} already exists')
        
        obj = SessionPrice.objects.create(doctor=doctor, duration=duration,type=type,price=price )
        obj.save()
        return validated_data