from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash

from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

from .forms import  UserRegistrationForm

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from tutorapp.models import VideoModel

# Create your views here.

def home_view(request):
    tutorials = VideoModel.objects.all()
    context = {'form':tutorials}
    
    return render(request, 'Home/Home.html', context)

@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You Logged out successfully!")
    return redirect('home-page')
  
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,'You have successfully Logged in!!!')
            return redirect('home-page')
        elif user is None:
            messages.error(request, "You Haven't an Acoount yet. Please Signup first.")
            return redirect(signup_view)
        else:
            messages.error(request,'Something Wrong happend, Try Again...')
    
    return render(request, 'LoginPage/LoginPage.html')
    
@permission_classes([AllowAny])
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home-page")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login-page')
        else:
            for error in list(form.errors.values()):
                print(request, error)
    else:
        form = UserRegistrationForm()
    return render(
        request = request,
        template_name = "SignUp/SignUp.html",
        context={"form":form}
        )
    
def send_email(subject, message, from_email, recipient_list):
    """
    Function to send email using Django's send_mail function.
    """
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True  # Email sent successfully
    except Exception as e:
        print(f"Error sending email: {e}")
        return False  # Email sending failed
    
def send_password(request):
    if request.method == 'POST':
        print(request.POST)
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")
        recipient = request.POST.get("recipient", "")
        
        user = User.objects.get(email=recipient)
        print('user',user)
        
        subject = subject+'heloo akhil'
        message = message+'Hello '+user.username+ ' Your Username is:'+user.username+' '+ user.password
        recipient_list = [recipient]
        print('sub',subject, 'msg',message, recipient_list)
        if subject and message and recipient_list:
            from_email = "webdevwithakhil989@gmail.com"  # Change to your recipient email address
            if send_email(subject, message, from_email, recipient_list):
                print('sub',subject, 'msg',message, recipient_list, from_email)
                print("Email sent successfully!")
                messages.success(request, 'Check Your Email, We have sent password to your email')
                return redirect('login-page')
            else:
                messages.error("Failed to send email. Please try again later.")
                return render(request, 'SendMail/SendMail.html')
        else:
            messages.error("Make sure all fields are entered and valid.")
            return render(request, 'SendMail/SendMail.html')
    else:
        return render(request, 'SendMail/SendMail.html')


@login_required   
def password_change(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif request.user is not None:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, data=request.POST)
            
            if form.is_valid():
                user=form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('password_change_done')
        else:
            messages.error(request, 'Failed to change password')
    else:
        messages.error(request, 'You Have no Account Signup first')
        return redirect('signup')
    form = PasswordChangeForm(user=request.user)
    return render(request,"PasswordChange/PasswordChange.html",
                  context={"form":form})
@login_required
def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

@login_required
def password_reset(request):
    form = PasswordResetForm()
    if request.method == "POST":
            form = PasswordResetForm(data=request.POST or None)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('password_change_done')
    else:
            messages.error(request, 'Failed to change password')
    print(form)
    return render(request, 'PasswordReset/PasswordReset.html')