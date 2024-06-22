from django.contrib import admin
from .models import User, Profile, TourGuide, Booking, Review

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(TourGuide)
admin.site.register(Booking)
admin.site.register(Review)
