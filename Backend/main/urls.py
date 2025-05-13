from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, CourseViewSet, SectionViewSet,
    CartViewSet,AttachmentViewSet, 
    #EnrollmentViewSet, PaymentViewSet,
    #CertificateViewSet
)
router= DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"course", CourseViewSet, basename="course")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r'sections', SectionViewSet)
router.register(r"attachments", AttachmentViewSet, basename="attachments")

urlpatterns = [
    
]

urlpatterns += router.urls