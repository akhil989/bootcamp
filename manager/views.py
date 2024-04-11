from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User, Group 

from tutorapp.models import VideoModel
from tutorapp.models import Order
from tutorapp.models import CartVideo


# Create your views here.

@login_required
@permission_classes([IsAdminUser])
def manager_dashboard(request):
    user = request.user.username
    print(user)
    user_name = get_object_or_404(User, username=user)
    manager_group = Group.objects.get(name='Manager')
    # print(manager_group.user_id)
    print(manager_group.user_set.all())
    if user_name in manager_group.user_set.all():
        print(f"{user_name} is a member of the Manager group")
        posts = VideoModel.objects.all().order_by('-created_at')
        cart = CartVideo.objects.all().order_by('-carted_at')
        order = Order.objects.all().order_by('-enrolled_at')
        users = User.objects.all().order_by('-date_joined')
        context = {'posts':posts, 'cart':cart, 'order':order,'users':users }
        return render(request, 'Manager/Manager.html', context)
    else:
        return redirect('home-page')