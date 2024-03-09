from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home_view, name='home-page'),
    path('login/', views.login_view, name='login-page'),
    path('logout/', views.logout_view, name='logout-page'),
    path('signup/', views.signup_view, name='signup-page'),
    path('send-password/', views.send_password, name='password-forget'),
    path('password_change/', views.password_change, name='password_change'),
    path('accounts/password_change/done/', views.password_change_done ,name='password_change_done'),
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
