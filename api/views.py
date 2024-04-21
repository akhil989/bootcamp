from django.shortcuts import render
from requests import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from rest_framework import status

from .serializers import MovieSerializer, UserSerializer
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


@api_view(['GET','POST'])
def login_view(request):
    if request.user.is_authenticated:
        return Response({'error': 'You are already logged in'}, status=400)

    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=400)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            serializer = UserSerializer(data=request.data)
            return Response(serializer)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
