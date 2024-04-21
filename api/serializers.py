from rest_framework import serializers
from .models import Movies
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movies
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']