from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    slug = models.SlugField(default='')
    name = models.CharField(max_length=255)

    def __str__(self)->str:
        return self.name
    
class Lecture(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Course(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Lecture, on_delete=models.CASCADE, default=None)
    content = models.TextField()

    def __str__(self):
        return self.title