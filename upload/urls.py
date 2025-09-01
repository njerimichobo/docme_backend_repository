from django.urls import path, include
from .views import UploadViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'upload', UploadViewSet, basename='upload')


urlpatterns = [
    path('', include(router.urls)),
]
