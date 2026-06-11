from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception as e:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )    
    