from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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


from tutorapp.models import VideoModel
from tutorapp.models import LikeVideo
from tutorapp.models import CartVideo
from tutorapp.models import Category
from tutorapp.models import RateVideo

from django.db.models import Count
from django.contrib.auth.models import AnonymousUser 

# Create your views here.

def home_view(request):
    pricelst=[]
    likes = LikeVideo.objects.all()
    if 'search' in request.GET:
        search_query = request.GET['search']
        tutorials_vid = VideoModel.objects.filter(title__icontains=search_query)
        print('search_query',search_query)
    elif 'search1' in request.GET:
        search_query = request.GET['search1']
        tutorials_vid = VideoModel.objects.filter(title__icontains=search_query)
        print('search_query',search_query)
    elif 'category' in request.GET:
        category_name = request.GET['category']
        tutorials_vid = VideoModel.objects.filter(category__name=category_name)
    else:
        tutorials_vid = VideoModel.objects.all().order_by('-created_at')
        
    if not isinstance(request.user, AnonymousUser):
        tutorials = VideoModel.objects.filter(carts__user=request.user)
        for item in tutorials:
            price = round(item.price)
            pricelst.append(price)
        total_cart = len(pricelst)
    else:
        total_cart = 0
    category = Category.objects.all()
    ratings = RateVideo.objects.all()
    context = {'form':tutorials_vid, 'likes':likes, 'total_cart': total_cart, 'category':category, 'ratings':ratings}
    return render(request, 'Home/Home.html', context)

@login_required
def cart_page(request):
    pricelst=[]
    tutorials = VideoModel.objects.filter(carts__user=request.user)
    for item in tutorials:
        price = round(item.price)
        pricelst.append(price)
    print('pricelst', pricelst, round(sum(pricelst)*1.2, 2))
    total_price = round(sum(pricelst)*1.2, 2)
    context = {'form':tutorials, 'total_price':total_price, 'total_cart':len(pricelst)}
    return render(request, 'CartPage/CartPage.html', context)

def cart_item_count(request):
    pricelst=[]
    tutorials = VideoModel.objects.filter(carts__user=request.user)
    for item in tutorials:
        price = round(item.price)
        pricelst.append(price)
    total_cart = len(pricelst)
    messages.info(request, f'{total_cart}')
    return render(request, 'NavBar/NavBar.html')


@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You Logged out successfully!")
    return redirect('home-page')

@login_required
def like_video(request, video_id):
    if request.method=='POST':
       video = VideoModel.objects.get(id=video_id)
       user = request.user
       liked = LikeVideo.objects.filter(user=user, video=video)
       if liked:
        liked.delete()
       else:
        LikeVideo.objects.create(user=user, video=video)
    return redirect('home-page')
@login_required
def cart_item(request, video_id):
    if request.method == 'POST':
        video = VideoModel.objects.get(id=video_id)
        user = request.user
        cart = CartVideo.objects.filter(user=user, video=video)
        if cart:
            cart.delete()
        else:
            CartVideo.objects.create(user=user, video=video)
    return redirect('home-page')
@login_required
def remove_cart_item(request, video_id):
    if request.method == 'POST':
        video = VideoModel.objects.get(id=video_id)
        user = request.user
        cart = CartVideo.objects.filter(user=user, video=video)
        if cart:
            cart.delete()
            # messages('Item Already in your cart!')
    return redirect('cart-page')
@login_required
def rate_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(VideoModel, id=video_id)
        user = request.user
        rating = request.POST.get('rating')  # Assuming your frontend sends the rating value
        rating = int(rating)
        print('rating+++==>', rating, type(rating))
        # Check if the user has already rated this video, if so, update the rating
        if rating is not None:
            try:
                user_rating, created = RateVideo.objects.get_or_create(user=user, video=video)
                user_rating.user_rating = rating
                user_rating.save()
                return redirect('home-page')
            except Exception as e:
                print('Rating error:', e)
                return JsonResponse({'error': 'Failed to save rating'}, status=500)
        else:
            return JsonResponse({'error': 'Rating value is missing'}, status=400)

    return  redirect('home-page')
    
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

def item_detail_page(request, id):
    details = VideoModel.objects.get(pk=id)
    context = {'details':details}
    return render(request, 'ItemDetailPage/ItemDetailPage.html', context)