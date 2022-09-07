from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class UsersFormsTests(TestCase):  
    def setUp(self):
        self.guest_client = Client()

    def test_user_create(self):
        users_object = User.objects.count()
        form_data = {
            'first_name': 'Тестовоеимя',
            'last_name': 'Тестоваяфамилия',
            'username': 'test',
            'email': 'test@test.ur',
            'password1': 'omta1234',
            'password2': 'omta1234',
        }
        response = self.guest_client.post(reverse('signup'),
                                      data=form_data, follow=True,)
        self.assertRedirects(response,
                             reverse('posts:index')
                             )
        self.assertEqual(User.objects.count(), users_object + 1,
                         'Ошибка в создании пользователя')
