from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import VideoFormModel

# Create your views here.

@login_required
def tutor_home(request):
    return render(request, 'Tutor/TutorHome.html')

@login_required
def tutor_signup_form(request):
    form = VideoFormModel()
    return render(request, 'TutorJoinForm/TutorJoinForm.html', {'form':form} )