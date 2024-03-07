from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.

def tutor_home(request):
    return render(request, 'Home/Home.html')
@login_required
def logout(request):
    try:
        logout(request)
        messages.info(request, "Logged out successfully!")
    except ValueError as e:
        if e:
            print(e)
    finally:
        return redirect('home')
    
   
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login( user)
            messages.success(request,'You have successfully Logged in!!!')
            return redirect('home')
        elif user is None:
            messages.error(request, "You Haven't an Acoount yet. Please Signup first.")
            return redirect(signup)
        else:
            messages.error(request,'Something Wrong happend, Try Again...')
    else:
        return render(request, 'LoginPage/LoginPage.html')

def signup(request):
    form = UserSignupForm()
    if request.method=='POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have Signed Up"))
            return redirect('home')
        else:
            messages.error(request, 'something wrong')
            return redirect('signup')
    else:
        return render(request, 'SignUp/SignUp.html',{"form":form} )