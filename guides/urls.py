from django.urls import path
from .views import profile, edit_profile, tour_guide_list, book_tour_guide, cancel_booking, user_profile

urlpatterns = [
    path('', profile, name='profile'),
    path('edit/', edit_profile, name='edit_profile'),
    path('guides/', tour_guide_list, name='tour_guide_list'),
    path('book/<int:guide_id>/', book_tour_guide, name='book_tour_guide'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('user/<int:user_id>/', user_profile, name='user_profile'),
]
