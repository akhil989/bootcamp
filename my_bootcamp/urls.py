from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home-page'),
    path('login/', views.login_view, name='login-page'),
    path('logout/', views.logout_view, name='logout-page'),
    path('signup/', views.signup_view, name='signup-page'),
    path('send-password/', views.send_password, name='password-forget')
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
