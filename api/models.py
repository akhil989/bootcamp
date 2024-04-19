from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import MAXYEAR
# Create your models here.
class Category(models.Model):
    slug = models.SlugField(default='')
    category = models.CharField(max_length =100, null=False)
class Movies(models.Model):
    name = models.CharField(max_length=100, null=False)
    year = models.IntegerField(validators=[MaxValueValidator(MAXYEAR),MinValueValidator(1850)], null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)