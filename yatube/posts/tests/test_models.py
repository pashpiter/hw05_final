from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='catJam',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        task_group = PostModelTest.group
        task_post = PostModelTest.post
        expected_group_name = str(task_group)
        expected_post_name = str(task_post)[:15]
        self.assertEqual(
            expected_group_name, task_group.title, 'Ошибка __str__'
        )
        self.assertEqual(
            expected_post_name, task_post.text, 'Ошибка __str__'
        )

    def test_verbose_name_group(self):
        """Проверяем verbose_name у модели Group"""
        task_group = PostModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'URL',
            'description': 'Описание группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_group._meta.get_field(value).verbose_name, expected,
                    'Ошибка в verbose_name у модели Group'
                )

    def test_verbose_name_post(self):
        """Проверяем verbose_name у модели Post"""
        task_post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_post._meta.get_field(value).verbose_name, expected,
                    'Ошибка в verbose_name у модели Post'
                )

    def test_help_text_group(self):
        """Проверяем help_text у модели Group"""
        task_group = PostModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'URL',
            'description': 'Описание группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_group._meta.get_field(value).help_text, expected,
                    'Ошибка в help_text у модели Group'
                )

    def test_help_text_post(self):
        """Проверяем help_text у модели Post"""
        task_post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_post._meta.get_field(value).help_text, expected,
                    'Ошибка в help_text у модели Post'
                )
