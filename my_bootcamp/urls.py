from django.urls import path
from . import views
urlpatterns = [
    path('', views.tutor_home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]
