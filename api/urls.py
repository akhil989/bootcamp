from django.urls import path, include
from rest_framework import routers
from .views import SampleViewset

# Instantiate the router
router = routers.SimpleRouter()

# Register the viewset with the router
router.register(r'movies', SampleViewset)

# URL patterns for the API app
urlpatterns = [
    path('', include(router.urls)),
]
