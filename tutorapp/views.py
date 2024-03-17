from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


from .forms import  VideoFormModel
from django.contrib.auth.models import User

# Create your views here.

@login_required
def tutor_home(request):
    name = request.session.get('name', '') 
    # user = request.session['session_data']
    print('username===',  name)
    return render(request, 'Tutor/TutorHome.html')

@login_required
def tutor_signup_form(request):
    user = request.user
    name = request.session.get('session_data', '') 
    print('username2===',  name)
    print('userdata2===',  user)
    form = VideoFormModel()
    if request.method == 'POST':
        form = VideoFormModel(request.POST, request.FILES)
        if form.is_valid():
            print('form_data', form.cleaned_data)
            try:
                instance = form
                instance.save()
                print("SAMPLE form",form.cleaned_data)
                form.save()
                return redirect('tutor-home')
            except Exception as e:
                if e:
                    raise Http404("Error")
            finally:
                print('files uploaded')
        else:
            form = VideoFormModel()
    return render(request, 'TutorJoinForm/TutorJoinForm.html', {'form':form} )

