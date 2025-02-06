from rest_framework import serializers
from .models import UserData

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['name', 'email', 'age']
        
    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value
        