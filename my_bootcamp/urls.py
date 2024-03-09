from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.home_view, name='home-page'),
    path('send-mail/', views.send_password, name='send-mail'),
    path('accounts/login/', views.login_view, name='login-page'),
    path('accounts/logout/', views.logout_view, name='logout-page'),
    path('accounts/signup/', views.signup_view, name='signup-page'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='PasswordChange/PasswordChange.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='PasswordChangeDone/PasswordChangeDone.html') ,name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='PasswordReset/PasswordReset.html'), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='PasswordResetDone/PasswordResetDone.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='PasswordResetConfirm/PasswordResetConfirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='PasswordResetComplete/PasswordResetComplete.html'), name='password_reset_complete')
    
   
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
