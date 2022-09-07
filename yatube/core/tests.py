from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class CoreTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = User.objects.create_user(username='user')

    def test_error_page(self):
        response = self.client.get('/nonexist-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')
