from django.core.paginator import Paginator  # Paginator sınıfını içe aktarın
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm, ProfileForm, TourGuideForm
from .models import Profile, TourGuide, Booking, User

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.create(user=user)
            if user.is_tour_guide:
                TourGuide.objects.create(profile=profile, languages='', experience=0)
            login(request, user)
            return redirect('profile')  # Başarılı kayıttan sonra yönlendirme
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})

@login_required
def profile(request):
    profile = request.user.profile
    tour_guide = None
    if hasattr(profile, 'tourguide'):
        tour_guide = profile.tourguide
    guide_bookings = Booking.objects.filter(tour_guide=request.user, status='active')
    traveler_bookings = Booking.objects.filter(traveler=request.user, status='active')
    return render(request, 'profile.html', {
        'profile': profile,
        'tour_guide': tour_guide,
        'guide_bookings': guide_bookings,
        'traveler_bookings': traveler_bookings,
    })

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    tour_guide = None
    if hasattr(profile, 'tourguide'):
        tour_guide = profile.tourguide
    guide_bookings = Booking.objects.filter(tour_guide=user, status='active')
    return render(request, 'user_profile.html', {
        'profile': profile,
        'tour_guide': tour_guide,
        'user': user,
        'guide_bookings': guide_bookings,
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    tour_guide = None
    if hasattr(profile, 'tourguide'):
        tour_guide = profile.tourguide

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        tour_guide_form = TourGuideForm(request.POST, instance=tour_guide)

        if profile_form.is_valid() and (not tour_guide or tour_guide_form.is_valid()):
            profile_form.save()
            if tour_guide:
                tour_guide_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)
        tour_guide_form = TourGuideForm(instance=tour_guide)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'tour_guide_form': tour_guide_form,
        'tour_guide': tour_guide
    })
    

def tour_guide_list(request):
    tour_guides = User.objects.filter(is_tour_guide=True)
    paginator = Paginator(tour_guides, 12)  # Her sayfada 12 tur rehberi
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tour_guide_list.html', {'page_obj': page_obj, 'current_user': request.user})

@login_required
def book_tour_guide(request, guide_id):
    tour_guide = User.objects.get(id=guide_id)
    if request.method == 'POST':
        booking = Booking.objects.create(
            tour_guide=tour_guide,
            traveler=request.user
        )
        return redirect('profile')
    return render(request, 'book_tour_guide.html', {'tour_guide': tour_guide})

@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.traveler == request.user:
        booking.status = 'cancelled'
        booking.save()
    return redirect('profile')
