from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    is_tour_guide = models.BooleanField(default=False)
    is_traveler = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='guides_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='guides_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

class TourGuide(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    languages = models.CharField(max_length=255, blank=True, default='')
    experience = models.IntegerField(default=0)
class Booking(models.Model):
    tour_guide = models.ForeignKey(User, related_name='guide_bookings', on_delete=models.CASCADE)
    traveler = models.ForeignKey(User, related_name='traveler_bookings', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    
class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
