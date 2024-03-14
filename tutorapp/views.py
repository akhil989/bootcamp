from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def tutor_home(request):
    return render(request, 'Tutor/TutorHome.html')

@login_required
def tutor_signup_form(request):
    return render(request, 'TutorJoinForm/TutorJoinForm.html' )