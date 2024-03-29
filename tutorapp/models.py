from datetime import timezone
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.http import request
from django.db.models import Avg

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(default='')
    name = models.CharField(max_length=255)

    def __str__(self)->str:
        return self.name

class VideoModel(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=False, upload_to='thumbnails', default='')
    video = models.FileField(null=False, upload_to='video', default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default='', related_name='instructors') 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
   

    def __str__(self):
        return self.title
    def total_likes(self):
        return LikeVideo.objects.filter(video=self).count()
    def liked_users(self):
        return [like.user.id for like in self.likes.all()]
    def liked_videos(self):
        return [like.video.id for like in self.likes.all()]
    def total_cart(self):
        return CartVideo.objects.filter(video=self).count()
    def cart_users(self):
        return [cart.user.id for cart in self.carts.all()]
    def price_after_commission(self):
        return round(self.price*Decimal(1.3),2)
    def total_rating(self):
        # Count the total number of ratings for this video
        return RateVideo.objects.filter(video=self).count()
    def average_rating(self):
        # Calculate the average rating for this video
        return RateVideo.objects.filter(video=self).aggregate(avg_rating=Avg('user_rating'))['avg_rating']
    def rated_users(self):
        return [user_rating.user.id for user_rating in self.rating.all()]
    def total_comments(self):
        return CommentTutorial.objects.filter(video=self).count()
    def user_comment(self):
        return [user_comment.user.id for user_comment in self.comments.all()]
    def instructor_list(self):
        return [instructor.user.id for instructor in self.instructors.all()]
class Course(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(VideoModel, on_delete=models.CASCADE, default=None)
    content = models.TextField()

    def __str__(self):
        return self.title
    
class FileModel(models.Model):
    file_name = models.CharField(max_length=10, null=False)
    # file_data = models.FileField(null=False, upload_to='file')    
    image_data = models.ImageField(null = False, upload_to='media')   
    created_at = models.DateTimeField(editable=False) 
    
class LikeVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='likes')
    
class CartVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='carts')

class RateVideo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='rating')
    user_rating = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user_rating)
class CommentTutorial(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=200) 
    
    def __str__(self):
        return self.comment