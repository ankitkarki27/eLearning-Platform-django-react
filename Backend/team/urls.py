from rest_framework.routers import DefaultRouter
from .views import TeamMemberViewSet

router = DefaultRouter()
router.register(r'team-members', TeamMemberViewSet)

urlpatterns = router.urls
