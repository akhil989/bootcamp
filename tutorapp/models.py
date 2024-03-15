from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    slug = models.SlugField(default='')
    name = models.CharField(max_length=255)

    def __str__(self)->str:
        return self.name
    
class VideoModel(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(null=False, upload_to='thumbnails', default='')
    video = models.FileField(null=False, upload_to='video', default='')
    pdf = models.FileField(null=False, upload_to='pdf', default='')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title
class Course(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(VideoModel, on_delete=models.CASCADE, default=None)
    content = models.TextField()

    def __str__(self):
        return self.title