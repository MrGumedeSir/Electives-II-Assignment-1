
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Activity

class BasicSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass12345')

    def test_home_page_loads(self):
        resp = self.client.get(reverse('fitbuddy:home'))
        self.assertEqual(resp.status_code, 200)

    def test_register_and_login(self):
        resp = self.client.post(reverse('fitbuddy:register'), {
            'username':'newuser','password1':'strongpass123','password2':'strongpass123','email':'a@b.com'
        }, follow=True)
        # registration should redirect to dashboard or login
        self.assertIn(resp.status_code, (200,302))
