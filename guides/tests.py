from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserLoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', is_traveler=True)
        self.profile = Profile.objects.create(user=self.user)
        
    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Giriş başarılı ise yönlendirme (302) beklenir

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Giriş başarısız ise form tekrar gösterilir
        self.assertContains(response, "Please enter a correct username and password")  # Hata mesajı kontrolü
