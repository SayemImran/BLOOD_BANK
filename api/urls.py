from django.urls import include, path
from rest_framework.routers import DefaultRouter
from bms.views import DonorProfileViewSet, BloodRequestViewSet, DonationHistoryViewSet, DonorProfileUpdateView

router = DefaultRouter()
router.register('donors', DonorProfileViewSet, basename='donor')
router.register('requests', BloodRequestViewSet, basename='request')
router.register('histories', DonationHistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # ✅ Donor can GET or PATCH their own profile (including image upload)
    path('donor/profile/', DonorProfileUpdateView.as_view(), name='donor-profile'),
]