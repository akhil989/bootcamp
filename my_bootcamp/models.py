
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from tutorapp.models import Course, VideoModel, CartVideo

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(VideoModel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length = 100, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)



    