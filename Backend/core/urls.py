
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("api/v1/", include("api.urls")),
    
     # JWT Authentication URLs (under api/v/)
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Users App APIs (under api/v1/)
    path('api/v1/users/', include('users.urls')), 
    
    # Listings App APIs
    # path('api/v1/listings/', include('listings.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
