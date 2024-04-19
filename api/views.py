from django.shortcuts import render
from requests import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import MovieSerializer
from .models import Movies 
# Create your views here.
class SampleViewset(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    
    @action(detail=True, methods=['post'])
    def post_movie(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return the serialized data of the newly created movie
        return Response(serializer.errors, status=400)  #
        