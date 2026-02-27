from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from bms.models import DonorProfile, BloodRequest, DonationHistory
from bms.serializers import BloodRequestSerializer, DonationHistorySerializer
from user.serializers import DonorProfileSerializer
from bms.permissions import IsAdminOrReadOnly, IsAdminOnlyDelete


# ─── Donor Profile Update View (for image upload) ─────────────────────────
class DonorProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = DonorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # ✅ fixed: was 'parsers'

    def get_object(self):
        return self.request.user.donor_profile


# ─── Donor Profile ViewSet ─────────────────────────────────────────────────
class DonorProfileViewSet(ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOnlyDelete]
    parser_classes = [MultiPartParser, FormParser]  # ✅ support image uploads

    @swagger_auto_schema(operation_summary="Donor Profile list")
    def list(self, request, *args, **kwargs):
        """Show all Donor Profiles"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create Donor Profile")
    def create(self, request, *args, **kwargs):
        """Create Donor Profile"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update Donor Profile Information")
    def update(self, request, *args, **kwargs):
        """Donor Profile Update"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete the donor profile - Admin Only")
    def destroy(self, request, *args, **kwargs):
        """Donor Profile DELETE (Admin Only)"""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Specific Donor Information")
    def retrieve(self, request, *args, **kwargs):
        """Get specific donor information"""
        return super().retrieve(request, *args, **kwargs)


# ─── Blood Request ViewSet ─────────────────────────────────────────────────
class BloodRequestViewSet(ModelViewSet):
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOnlyDelete]

    def get_queryset(self):
        return BloodRequest.objects.filter(is_active=True).exclude(recipient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(recipient=self.request.user)

    @swagger_auto_schema(operation_summary="Retrieve active blood requests")
    def list(self, request, *args, **kwargs):
        """Show all active blood requests"""
        return super().list(request, *args, **kwargs)  # ✅ fixed: was super().create()

    @swagger_auto_schema(operation_summary="Create a blood request")
    def create(self, request, *args, **kwargs):
        """Create a new blood request"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a specific blood request")
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific blood request"""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update request")
    def update(self, request, *args, **kwargs):
        """Update a blood request"""
        return super().update(request, *args, **kwargs)  # ✅ fixed: was super().create()

    @swagger_auto_schema(operation_summary="Delete request (Admin Only)")
    def destroy(self, request, *args, **kwargs):
        """Delete a blood request"""
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a blood request and log donation history"""
        blood_request = self.get_object()

        # ✅ Prevent donor from accepting their own request
        if blood_request.recipient == request.user:
            return Response(
                {"error": "You cannot donate to your own blood request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Prevent accepting an already closed request
        if not blood_request.is_active:
            return Response(
                {"error": "This blood request is no longer active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        DonationHistory.objects.create(
            donor=request.user,
            request=blood_request,
            status='donated'
        )

        blood_request.is_active = False
        blood_request.save()

        return Response({"message": "Blood request accepted successfully"})


# ─── Donation History ViewSet ──────────────────────────────────────────────
class DonationHistoryViewSet(ModelViewSet):
    serializer_class = DonationHistorySerializer
    permission_classes = [IsAuthenticated, IsAdminOnlyDelete]

    def get_queryset(self):
        return DonationHistory.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

    @swagger_auto_schema(operation_summary="Show all donation history")
    def list(self, request, *args, **kwargs):
        """Show all blood donation activity"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update the donation status")
    def update(self, request, *args, **kwargs):
        """Update donation status"""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete Donation history - Admin Only")
    def destroy(self, request, *args, **kwargs):
        """Delete the donation history (Admin Only)"""
        return super().destroy(request, *args, **kwargs)