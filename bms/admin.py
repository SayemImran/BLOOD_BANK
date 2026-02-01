from django.contrib import admin
from bms.models import DonorProfile, BloodRequest, DonationHistory

admin.site.register(DonorProfile)
admin.site.register(BloodRequest)
admin.site.register(DonationHistory)
