from rest_framework import serializers
from .models import VideoModel

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ['title','thumbnail','video','category','price','description']