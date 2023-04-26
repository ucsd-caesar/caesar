from rest_framework import routers
from .viewsets import MarkerViewSet

router = routers.DefaultRouter()
router.register(r"markers", MarkerViewSet, basename="marker")

urlpatterns = router.urls