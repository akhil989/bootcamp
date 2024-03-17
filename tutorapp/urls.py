from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutor_home, name='tutor-home'),
    path('join-now/', views.tutor_signup_form, name='join-now'),
   
]
