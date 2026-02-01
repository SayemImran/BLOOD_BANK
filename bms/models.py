from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class DonorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donor_profile')
    image = CloudinaryField('image', blank=True, null=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} ({self.user.blood_group})"

class BloodRequest(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.CharField(max_length=3)
    location = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description[:25]}"


class DonationHistory(models.Model):
    STATUS = [
        ('donated', 'Donated'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='donations')
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='histories')
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True)
