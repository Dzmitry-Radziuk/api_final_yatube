from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Модель для группы с названием, слагом и описанием.
    """
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """Возвращает название группы."""
        return self.title


class Post(models.Model):
    """
    Модель для поста с текстом, автором, датой и изображением.
    """
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts',
        blank=True, null=True,
        verbose_name='Группа'
    )

    def __str__(self):
        """Возвращает текст поста."""
        return self.text


class Comment(models.Model):
    """
    Модель для комментария с автором, постом и текстом.
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        """Возвращает комментарий с автором и постом."""
        return f'Комментарий от {self.author.username} к посту {self.post.id}'


class Follow(models.Model):
    """
    Модель для подписки с пользователем и его подписчиком.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        unique_together = ('user', 'following')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """Возвращает строку подписки."""
        return f'{self.user} подписан на {self.following}'
