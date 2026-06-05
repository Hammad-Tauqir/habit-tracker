from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import generics
# Create your views here.
class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        extra_kwargs={
            'password':{'write_only':True}

        }
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    # Register API
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    queryset=User.objects.all()
    