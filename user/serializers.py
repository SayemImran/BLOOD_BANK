from rest_framework import serializers
from user.models import CustomUser
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from bms.models import DonorProfile


class UserCreateSerializer(BaseUserCreateSerializer):
    image = serializers.ImageField(required=False, allow_null=True, write_only=True)
    last_donation_date = serializers.DateField(required=False, allow_null=True, write_only=True)
    is_available = serializers.BooleanField(required=False, default=True, write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'age', 'address', 'blood_group', 'gender',
            'image', 'last_donation_date', 'is_available',
        ]

    def validate(self, attrs):
        # ✅ Stash DonorProfile fields on the instance before Djoser touches attrs
        self._donor_image = attrs.pop('image', None)
        self._donor_last_donation_date = attrs.pop('last_donation_date', None)
        self._donor_is_available = attrs.pop('is_available', True)
        return super().validate(attrs)

    def create(self, validated_data):
        # ✅ validated_data is now clean — only CustomUser fields
        user = super().create(validated_data)

        # ✅ Use the stashed DonorProfile fields
        profile_data = {
            'user': user,
            'last_donation_date': self._donor_last_donation_date,
            'is_available': self._donor_is_available,
        }
        if self._donor_image:
            profile_data['image'] = self._donor_image

        DonorProfile.objects.get_or_create(user=user, defaults={
        'last_donation_date': self._donor_last_donation_date,
        'is_available': self._donor_is_available,
        **({'image': self._donor_image} if self._donor_image else {})
        })
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = "CustomUserSerializer"


class DonorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    age = serializers.IntegerField(source='user.age', read_only=True)
    address = serializers.CharField(source='user.address', read_only=True)
    blood_group = serializers.CharField(source='user.blood_group', read_only=True)
    gender = serializers.CharField(source='user.gender', read_only=True)

    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = DonorProfile
        fields = [
            'id', 'user', 'name', 'age', 'address',
            'blood_group', 'gender', 'image',
            'last_donation_date', 'is_available',
        ]

    def to_representation(self, instance):
        # ✅ On read, return Cloudinary URL instead of raw image field
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url if instance.image else None
        return rep