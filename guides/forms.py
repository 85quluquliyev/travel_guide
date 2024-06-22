from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, TourGuide

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_tour_guide', 'is_traveler']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

class TourGuideForm(forms.ModelForm):
    class Meta:
        model = TourGuide
        fields = ['languages', 'experience']
