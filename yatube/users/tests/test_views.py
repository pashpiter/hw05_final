from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..forms import CreationForm

User = get_user_model()


class UsersViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_user_signup_page_show_correct_context(self):
        """Шаблон user signup сформирован с правильным контекстом."""
        expected_klass = CreationForm
        response = self.guest_client.get(
            reverse('signup')
        )
        field_klass = response.context['form']
        self.assertIsInstance(field_klass, expected_klass)
