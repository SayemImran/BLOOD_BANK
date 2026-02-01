from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
     BLOOD_GROUPS = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ]

     GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
     ]
     age = models.PositiveIntegerField(default=18)
     address = models.TextField()
     image = CloudinaryField('image', blank=True, null=True)
     last_donation_date = models.DateField(null=True, blank=True)
     is_available = models.BooleanField(default=True)
     blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
     gender = models.CharField(max_length=10, choices=GENDERS)

     def __str__(self):
            return self.get_full_name()