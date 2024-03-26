from datetime import timezone
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.http import request
# Create your models here.

class Category(models.Model):
    slug = models.SlugField(default='')
    name = models.CharField(max_length=255)

    def __str__(self)->str:
        return self.name
class Ratings(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1) 
    
    def __str__(self) -> str:
        return self.rating
class VideoModel(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=False, upload_to='thumbnails', default='')
    video = models.FileField(null=False, upload_to='video', default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default='') 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    rating = models.ForeignKey(Ratings, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    def total_likes(self):
        return LikeVideo.objects.filter(video=self).count()
    def liked_users(self):
        return [like.user.id for like in self.likes.all()]
    def total_cart(self):
        return CartVideo.objects.filter(video=self).count()
    def cart_users(self):
        return [cart.user.id for cart in self.carts.all()]
    def price_after_commission(self):
        return round(self.price*Decimal(1.3),2)
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