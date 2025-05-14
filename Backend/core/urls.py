
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from users.views import UserAccountViewSet

urlpatterns = [
      path('admin/', admin.site.urls),
    #API v1 routes
    path('api/v1/', include([
        
        # App routes
        path('users/', include('users.urls')), 
        path('main/', include('main.urls')),
        path('team/', include('team.urls')),

        # Auth routes
        path('auth/',include([
            path('register/', UserAccountViewSet.as_view({'post': 'create'}), name='register'),
            path('login/', TokenObtainPairView.as_view(), name='login'),
            path('logout/', TokenBlacklistView.as_view()),
        ])),
        
        # token endpoints
        path('token/', include([
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            path('verify/', TokenVerifyView.as_view(), name='token_verify'),

        ]))
]))
 ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    