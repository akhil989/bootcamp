from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User

from tutorapp.models import VideoModel
from tutorapp.models import Order
from tutorapp.models import CartVideo

# Create your views here.
@login_required
def manager_dashboard(request):
    posts = VideoModel.objects.all().order_by('-created_at')
    cart = CartVideo.objects.all().order_by('-carted_at')
    order = Order.objects.all().order_by('-enrolled_at')
    users = User.objects.all().order_by('-date_joined')
    context = {'posts':posts, 'cart':cart, 'order':order,'users':users }
    return render(request, 'Manager/Manager.html', context)