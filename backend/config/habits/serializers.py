from rest_framework import serializers
from .models import Habit, HabitCompletion

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Habit
        fields='__all__'
        read_only_fields=['user']

class HabitCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model= HabitCompletion
        fields='__all__'
        read_only_fields=['habit']