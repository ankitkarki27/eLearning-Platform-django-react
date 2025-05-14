from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView 
)
from .views import UserAccountViewSet

router = DefaultRouter()
router.register("", UserAccountViewSet, basename="user")

urlpatterns = [
    
]
urlpatterns += router.urls