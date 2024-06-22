from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from guides.views import register, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('profile/', include('guides.urls')),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
]
