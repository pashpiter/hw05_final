from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_authorized_client__exists_at_desired_location(self):
        """URL-адрес доступен по соответствующему
        адресу для авторизованных пользоателей."""
        url_names = (
            reverse('password_change'),
            reverse('password_change_done'),
            reverse('logout'),
            reverse('signup'),
            reverse('login'),
        )
        for address in url_names:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK,
                                 'Ошибка в доступе к страницам!')

    def test_urls_guest_client__exists_at_desired_location(self):
        """URL-адрес доступен по соответствующему
        адресу для не авторизованных пользоателей."""
        url_names = (
            reverse('signup'),
            reverse('login'),
        )
        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK,
                                 'Ошибка в доступе к страницам!')

    def test_urls_for_authorized_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'users/password_change_form.html': (reverse(
                                                'password_change')),
            'users/password_change_done.html': (reverse(
                                                'password_change_done')),
            'users/logged_out.html': (reverse('logout')),
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template,
                                        'Ошибка в доступе к шаблонам!')

    def test_urls_for_guest_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'users/login.html': (reverse('login')),
            'users/signup.html': (reverse('signup')),
            'users/password_reset_form.html': (reverse('password_reset')),
            'users/password_reset_done.html': (reverse(
                'password_reset_done')),
            'users/password_reset_complete.html': (reverse(
                'password_reset_complete')),
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template,
                                        'Ошибка в доступе к шаблонам!')
