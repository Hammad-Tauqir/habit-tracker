from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Habit(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_completed=models.BooleanField(default=False)
    # Streak Data
    current_streak= models.IntegerField(default=0)
    longest_streak= models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class HabitCompletion(models.Model):
    habit=models.ForeignKey(Habit,on_delete=models.CASCADE,related_name='completions')
    completed_at=models.DateField(default=now)

    class Meta:
        unique_together=['habit','completed_at']

    def __str__(self):
        return f"{self.habit.name}-{self.completed_at}"    

