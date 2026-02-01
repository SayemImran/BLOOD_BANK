from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import CustomUser
from bms.models import DonorProfile, BloodRequest, DonationHistory
from bms.serializers import BloodRequestSerializer,DonationHistorySerializer
from user.serializers import DonorProfileSerializer
from bms.permissions import IsAdminOrReadOnly, IsAdminOnlyDelete
from drf_yasg.utils import swagger_auto_schema



class DonorProfileViewSet(ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes =[IsAuthenticated,IsAdminOnlyDelete]

    @swagger_auto_schema(operation_summary=" Donor Profile list")
    def list(self, request, *args, **kwargs):
        """Show all Donor Profile"""
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Create Donor Profile")
    def create(self, request, *args, **kwargs):
        """Create Donor Profile """
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Update donor Profile Information")
    def update(self, request, *args, **kwargs):
        """ Donor Profile Update"""
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Delete the donor profile - Admin Only")
    def destroy(self, request, *args, **kwargs):
        """ Donor Profile DELETE (Admin Only)"""
        return super().destroy(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Specific Donor Information")
    def retrieve(self, request, *args, **kwargs):
        """ get the specific donor Information"""
        return super().retrieve(request, *args, **kwargs)

class BloodRequestViewSet(ModelViewSet):
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOnlyDelete]

    @swagger_auto_schema(operation_summary="Retrieve active blood requests")
    def list(self, request, *args, **kwargs):
        """ Show all request for blood """
        return super().create(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Retrieve a specific blood request")
    def retrieve(self, request, *args, **kwargs):
        """ Retrieve a specific blood request """
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Update request")
    def update(self,request,*args,**kwargs):
        return super().create(request,*args,**kwargs)
    @swagger_auto_schema(operation_summary="delete request (Only Admin)")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    def get_queryset(self):
        return BloodRequest.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        blood_request = self.get_object()

        DonationHistory.objects.create(
            donor=request.user,
            request=blood_request,
            status='donated'
        )

        blood_request.is_active = False
        blood_request.save()

        return Response({"message": "Blood request accepted successfully"})


class DonationHistoryViewSet(ModelViewSet):
    serializer_class = DonationHistorySerializer
    permission_classes = [IsAuthenticated,IsAdminOnlyDelete]

    def get_queryset(self):
        return DonationHistory.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

    @swagger_auto_schema(operation_summary="Show all blood requests")
    def list(self, request, *args, **kwargs):
        """
        Show all blood donation activity
        """
        return super().list(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Update the donation status")
    def update(self, request, *args, **kwargs):
        """ Update donation status"""
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(operation_summary="Delete Donation history - Admin Only")
    def destroy(self, request, *args, **kwargs):
        """Delete the donation history (Admin Only)"""
        return super().destroy(request, *args, **kwargs)