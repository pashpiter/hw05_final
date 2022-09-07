from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_authorized_client__exists_at_desired_location(self):
        """URL-адрес доступен по соответствующему
        адресу для всех пользоателей."""
        url_names = (
            reverse('about:author'),
            reverse('about:tech'),
        )
        clients = (self.guest_client, self.authorized_client)
        for client in clients:
            for address in url_names:
                with self.subTest(address=address):
                    response = client.get(address)
                    self.assertEqual(response.status_code, HTTPStatus.OK,
                                     'Ошибка в доступе к страницам!')
