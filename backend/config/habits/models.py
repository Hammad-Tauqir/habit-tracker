from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_completed=models.BooleanField(default=False)

    def __str__(self):
        return self.name

