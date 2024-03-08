from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('send-password/', views.send_password, name='password-forget')
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
