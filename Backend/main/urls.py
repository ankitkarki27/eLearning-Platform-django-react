from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router= DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    
]

urlpatterns += router.urls