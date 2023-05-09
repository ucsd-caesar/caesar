from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()
router.register(r"markers", MarkerViewSet, basename="marker")
router.register(r"agencies", AgencyViewSet, basename="agency")
router.register(r"user", UserViewSet, basename="user")
router.register(r"livestreams", LivestreamViewSet, basename="livestream")
router.register(r"viewports", ViewportViewSet, basename="viewport")

urlpatterns = router.urls