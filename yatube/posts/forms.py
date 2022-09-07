from django.forms import ModelForm, forms
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {'text': 'Текст поста',
                  'group': 'Группа',
                  'image': 'Изображение'}
        help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу, в которой будет опубликован пост',
            'image': 'Добавьте картинку к посту (необязательно)'
        }

        def clean_text(self):
            data = self.cleaned_data['text']
            if data == '':
                raise forms.ValidationError(
                    'Необходимо заполнить текстовое поле!')
            return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = {'text'}
        labels = {'text': 'Текст комментария'}
        help_texts = {'text': 'Текст комментария'}

        def clean_text(self):
            data = self.cleaned_data['text']
            if data == '':
                raise forms.ValidationError(
                    'Необходимо заполнить поле комментария!')
            return data
