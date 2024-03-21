from datetime import timezone
from site import USER_BASE
from django.db import models
from django.contrib.auth.models import User
from django.http import request
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
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default='') 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title
    def total_likes(self):
        return LikeVideo.objects.filter(video=self).count()
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
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE)