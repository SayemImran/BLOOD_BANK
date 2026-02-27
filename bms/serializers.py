from rest_framework import serializers
from .models import DonorProfile, BloodRequest, DonationHistory


class BloodRequestSerializer(serializers.ModelSerializer):
    # ✅ Shows donor's full name instead of exposing full user object
    recipient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BloodRequest
        fields = ['id', 'recipient', 'blood_group', 'location', 'description', 'is_active', 'created_at']
        read_only_fields = ['recipient', 'created_at']


class DonationHistorySerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DonationHistory
        fields = ['id', 'donor', 'request', 'status', 'date']
        read_only_fields = ['donor', 'date']