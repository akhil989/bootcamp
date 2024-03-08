from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes

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

# Create your views here.

def home_view(request):
    return render(request, 'Home/Home.html')

@permission_classes([IsAuthenticated])
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You Logged out successfully!")
    return redirect('home')
  
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,'You have successfully Logged in!!!')
            return redirect('home')
        elif user is None:
            messages.error(request, "You Haven't an Acoount yet. Please Signup first.")
            return redirect(signup_view)
        else:
            messages.error(request,'Something Wrong happend, Try Again...')
    else:
        return render(request, 'LoginPage/LoginPage.html')
    
@permission_classes([AllowAny])
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
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
        recipient_list = [recipient]
        print('sub',subject, 'msg',message, recipient_list)
        if subject and message and recipient_list:
            from_email = "webdevwithakhil989@gmail.com"  # Change to your recipient email address
            if send_email(subject, message, from_email, recipient_list):
                print('sub',subject, 'msg',message, recipient_list, from_email)
                print("Email sent successfully!")
                return HttpResponse("Email sent successfully!")
            else:
                return HttpResponse("Failed to send email. Please try again later.")
        else:
            return HttpResponse("Make sure all fields are entered and valid.")
    else:
        return render(request, 'SendMail/SendMail.html')


    
# def send_email(request):  
#    if request.method == "POST": 
#        with get_connection(  
#            host=settings.EMAIL_HOST, 
#         port=settings.EMAIL_PORT,  
#         username=settings.EMAIL_HOST_USER, 
#         password=settings.EMAIL_HOST_PASSWORD, 
#         use_tls=settings.EMAIL_USE_TLS  
#        ) as connection:  
#            subject = request.POST.get("subject")  
#            email_from = settings.EMAIL_HOST_USER  
#            recipient_list = [request.POST.get("email"), ]  
#            message = request.POST.get("message")  
#            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
 
#    return render(request, 'SendMail/SendMail.html')