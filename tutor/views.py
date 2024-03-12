from django.shortcuts import render

# Create your views here.


def tutor_home(request):
    return render(request, 'Tutor/TutorHome.html')