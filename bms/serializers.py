from rest_framework import serializers
from user.models import CustomUser
from .models import DonorProfile, BloodRequest, DonationHistory
from user.serializers import UserSerializer

class BloodRequestSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    class Meta:
        model = BloodRequest
        fields = ['id', 'recipient', 'blood_group', 'location', 'description', 'is_active', 'created_at']


class DonationHistorySerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DonationHistory
        fields = ['id', 'donor', 'request', 'status', 'date']
        read_only_fields = ['donor', 'date']