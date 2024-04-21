from django.urls import path, include
from rest_framework import routers
from .views import SampleViewset
from. import views
from django.contrib.auth import views as auth_views

# Instantiate the router
router = routers.SimpleRouter()

# Register the viewset with the router
router.register(r'movies', SampleViewset)

# URL patterns for the API app
urlpatterns = [
    path('', include(router.urls)),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='LoginPage/LoginPage.html'), name='login-page'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='LogOut/LogOut.html'), name='logout-page'),
    # path('accounts/signup/', views.signup_view, name='signup-page'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='PasswordChange/PasswordChange.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='PasswordChangeDone/PasswordChangeDone.html') ,name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='PasswordReset/PasswordReset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='PasswordResetDone/PasswordResetDone.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='PasswordResetConfirm/PasswordResetConfirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='PasswordResetComplete/PasswordResetComplete.html'), name='password_reset_complete'),

]
