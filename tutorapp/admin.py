from django.contrib import admin
from .models import Category
from .models import Course
from .models import VideoModel
from .models import LikeVideo
from .models import CartVideo
from .models import CommentTutorial
from .models import Order
from .models import RateVideo
from .models import FlagedVideo
# Register your models here.


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(VideoModel)
admin.site.register(LikeVideo)
admin.site.register(CartVideo)
admin.site.register(CommentTutorial)
admin.site.register(Order)
admin.site.register(RateVideo)
admin.site.register(FlagedVideo)