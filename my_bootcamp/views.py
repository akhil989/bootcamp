import decimal
import http
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.utils.html import format_html

from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

from .forms import  UserRegistrationForm
from tutorapp.forms import VideoFormModel
from tutorapp.forms import CommentForm


from tutorapp.models import VideoModel
from tutorapp.models import LikeVideo
from tutorapp.models import CartVideo
from tutorapp.models import Category
from tutorapp.models import RateVideo
from tutorapp.models import CommentTutorial
from tutorapp.models import Order


from django.db.models import Count
from django.contrib.auth.models import AnonymousUser 

import razorpay
import os
from dotenv import load_dotenv

# Create your views here.

def home_view(request):
    pricelst=[]
    likes = LikeVideo.objects.all()
    if 'search' in request.GET:
        search_query = request.GET['search']
        tutorials_vid = VideoModel.objects.filter(title__icontains=search_query)
        if len(tutorials_vid) == 0:
            messages.info(request, f"{request.user}, There is no post of your search term, Try another search")
    elif 'search1' in request.GET:
        search_query = request.GET['search1']
        tutorials_vid = VideoModel.objects.filter(title__icontains=search_query)
        if len(tutorials_vid) == 0:
            messages.info(request, f"{request.user}, There is no post of your search term, Try another search")
    elif 'search_instructor' in request.GET:
        search_query = request.GET['search_instructor']
        tutorials_vid = VideoModel.objects.filter(instructor_id=search_query)
        instructor_data = get_object_or_404(User, id=int(search_query))
        messages.info(request, f"Tutorials posted by {instructor_data}")
    elif 'category' in request.GET:
        category_name = request.GET['category']
        tutorials_vid = VideoModel.objects.filter(category__name=category_name)
    elif 'category_like' in request.GET:
        category_name = request.GET['category_like']
        tutorials_vid = VideoModel.objects.filter(likes__user=request.user)
        if len(tutorials_vid) == 0:
            messages.info(request, f"{request.user}, You have no liked posts to display")
        else:
            messages.info(request, f"Tutorials liked by {request.user}")
    elif 'category_cart' in request.GET:
        category_name = request.GET['category_cart']
        tutorials_vid = VideoModel.objects.filter(carts__user=request.user)
        if len(tutorials_vid) == 0:
            messages.info(request, f"{request.user}, You have no cart items to display")
        else:
            messages.info(request, f"Tutorials carted by {request.user}")
    elif 'category_rated' in request.GET:
        category_name = request.GET['category_rated']
        tutorials_vid = VideoModel.objects.filter(rating__user=request.user)
        if len(tutorials_vid) == 0:
            messages.info(request, f"{request.user}, You have no rated posts to display")
        else:
            messages.info(request, f"Tutorials rated by {request.user}")
    elif 'category_posts' in request.GET:
        category_name = request.GET['category_posts']
        tutorials_vid = VideoModel.objects.filter(instructor=request.user)
        print('len',len(tutorials_vid))
        if len(tutorials_vid) == 0:
           messages.info(request, format_html("{} You have not posted yet, start tutoring here <a href='{}' class='underline text-violet-700'>Post Your Tutorial</a>", request.user, "http://localhost:8000/tutor/join-now/"))
        else:
            messages.info(request, f"Tutorials posted by {request.user}")
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
    print('pricelst', pricelst, round(sum(pricelst), 2))
    total_price = round(sum(pricelst)*1, 2)
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
    return redirect('cart-page')
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
                messages.success(request, 'You Have rated this item')
                return redirect('item-details', video_id)
            except Exception as e:
                print('Rating error:', e)
                messages.error(request, 'Error')
                return redirect('item-details',video_id)
        else:
            messages.info(request, 'Rating value is missing')
            return redirect('item-details')

    return  redirect('item-details')
    
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
    details = get_object_or_404(VideoModel, pk=id)
    if request.method == 'POST':
        video = details
        user = request.user
        comment = request.POST.get('comment')  # Assuming your frontend sends the rating value
        print('rating+++==>', comment, type(comment))
        # Check if the user has already rated this video, if so, update the rating
        if comment :
            try:
                # Create a new comment instance
                comment = CommentTutorial.objects.get_or_create(user=user, video=video, comment=comment)
                messages.success(request,'Your Comment Posted.')
                return redirect('item-details', id=id)  
            except Exception as e:
                print('Comment error:', e)
                messages.error(request,'Error Posing Comment')
                return redirect('item-details', id=id)
        else:
            messages.info(request, 'Comment Missing')
            return redirect('item-details', id=id)
    context = {'details':details}
    print('comments',)
    return render(request, 'ItemDetailPage/ItemDetailPage.html', context)

# delete page
@login_required
def item_delete_page(request, id):
    item = get_object_or_404(VideoModel, pk=id)
    context = {'item':item}
    if request.method == 'POST':
        if 'delete' in request.POST:
            return redirect('delete-file', id=id)
    return render(request, 'ItemDelete/ItemDelete.html', context)

# update post
@login_required
def item_update_page(request, id):
    item = get_object_or_404(VideoModel, pk=id)
    update_form = VideoFormModel(instance=item )
    context = {'item':item, 'form':update_form}
    if request.method == 'POST':
        if 'update' in request.POST:
            # return redirect('update-file', id=id)
            update_form = VideoFormModel(request.POST, instance=item )
            if update_form.is_valid():
                print("update:",update_form.cleaned_data)
                update_form.save()
                messages.success(request, 'Successfully Updated Your Post')
                return redirect('http://localhost:8000/?category_posts=category_posts/')
            else:
                messages.error(request, 'Error updating post...')
                update_form = VideoFormModel()
            return render(request, 'ItemUpdate/ItemUpdate.html', context)
    return render(request, 'ItemUpdate/ItemUpdate.html', context)


# delete function
@login_required
def delete_file(request,id):
    try:
        f = get_object_or_404(VideoModel, pk=id)
        image = str(f.thumbnail)  # Convert the image field to a string
        image_path = f.thumbnail.path  # Get the absolute path of the image
        video_path = f.video.path
        f.delete()

        if os.path.exists(image_path):
            os.remove(image_path)
            print('File deleted from folder')
        else:
            print('Path does not exist')
        if os.path.exists(video_path):
            os.remove(video_path)
            print('File deleted from folder')
        else:
            print('Path does not exist')
    except VideoModel.DoesNotExist:
        print('File not found') 
    return redirect('http://localhost:8000/?category_posts=category_posts/')
# update function
@login_required
def update_file(request, id):
    item = get_object_or_404(VideoModel, pk=id)
    if request.method == 'POST':
        update_form = VideoFormModel(request.POST, instance=item )
        if update_form.is_valid():
            try:
                    print("update:",update_form.cleaned_data)
                    update_form.save()
                    messages.success(request, 'Successfully Updated Your Post')
                    return redirect('http://localhost:8000/?category_posts=category_posts/')
            except:
                    messages.error(request, 'Error updating post...')
                    update_form = VideoFormModel()
                    return redirect('http://localhost:8000/?category_posts=category_posts/')

# enrollments
load_dotenv()
@login_required
def item_purchase(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        price = decimal.Decimal(request.POST.get('price')) * 100

        razorpay_key = "rzp_test_kaz60tEn560E6V"
        razorpay_secret = "JpovtSP6RXXSV5iB95SwcTDr"

        try:
            client = razorpay.Client(auth=(razorpay_key, razorpay_secret))
            response_payment = client.order.create(dict(amount=int(price), currency='INR'))
            print('payment', response_payment)
            order_id = response_payment['id']
            order_status = response_payment['status']
            if order_status == 'created':
                order = Order.objects.create(
                    student_id=user_id,
                    course_id=course_id,
                    price=price / 100,  # Convert back to Decimal
                    order_id=order_id,
                )
                orderid = order.order_id
                return redirect('payment', order_id)

        except Exception as e:
            # Log the error or provide a user-friendly message
            print("Razorpay API request failed:", e)
            # Optionally, redirect the user to an error page or display a message
            return redirect('cart-page', {'message': 'Razorpay API request failed. Please try again later.'})
        print('payment', response_payment)
    return redirect('cart-page')

def razorpay_page(request, order_id):
    order = Order.objects.get(order_id=order_id)
    context = {'order': order}
    print('jjf',order.order_id, order.student_id)
    return render(request, 'Razorpay/Razorpay.html', context)

def razorpay_success(request):
    response = request.POST
    print(response)
    return render(request, 'PaymentSuccess/PaymentSuccess.html')