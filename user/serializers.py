from rest_framework import serializers
from user.models import CustomUser
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from bms.models import DonorProfile
from django.contrib.auth import get_user_model


class UserCreateSerializer(BaseUserCreateSerializer):
    image = serializers.ImageField()
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'age', 'address','blood_group','gender','image','last_donation_date','is_available']

        def create(self, validated_data):
            user = super().create(validated_data)
            image = validated_data.pop('image')
            last_donation_date = validated_data.pop('last_donation_date', None)
            is_available = validated_data.pop('is_available', True)
            DonorProfile.objects.create(
                user=user,
                image=image,
                last_donation_date=last_donation_date,
                is_available=is_available
            )
            return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'email']
        ref_name = "CustomUserSerializer"


class DonorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    age = serializers.CharField(source='user.age', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    blood_group = serializers.CharField(source='user.blood_group', read_only=True)
    gender = serializers.CharField(source='user.gender', read_only=True)
    image = serializers.ImageField()
    class Meta:
        model = DonorProfile
        fields = [
            'id',
            'user', 
            'name',
            'age',
            'address',
            'blood_group',
            'gender',
            'image', 
            'last_donation_date', 
            'is_available'
        ]
    