from django.urls import include, path
from rest_framework.routers import DefaultRouter
from bms.views import DonorProfileViewSet, BloodRequestViewSet, DonationHistoryViewSet
from datetime import timedelta
from pathlib import Path
router = DefaultRouter()
router.register('donors', DonorProfileViewSet, basename='donor')
router.register('requests', BloodRequestViewSet, basename='request')
router.register('histories', DonationHistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]