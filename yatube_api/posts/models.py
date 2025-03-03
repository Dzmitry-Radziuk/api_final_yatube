from django.contrib.auth import get_user_model
from django.db import models
from posts.constants import MAX_LENGTH_STR, MAX_LENGTH_TEXT

User = get_user_model()


class Group(models.Model):
    """Модель для группы с названием, слагом и описанием."""

    title = models.CharField(
        max_length=200,
        verbose_name='Название группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )
    description = models.TextField(
        verbose_name='Описание группы'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        default_related_name = 'groups'

    def __str__(self):
        """Возвращает название группы."""
        return self.title[:30]


class Post(models.Model):
    """Модель для поста с текстом, автором, датой и изображением."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Группа'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        default_related_name = 'posts'
        ordering = ['-pub_date']

    def __str__(self):
        """Возвращает текст поста."""
        return (f'Пост {self.text[:MAX_LENGTH_TEXT]}'
                f'от автора: {self.author.username[:MAX_LENGTH_STR]}'
                )


class Comment(models.Model):
    """Модель для комментария с автором, постом и текстом."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментарий'
    )
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ['created']

    def __str__(self):
        """Возвращает комментарий с автором и постом."""
        return (f'Комментарий от {self.author.username[:MAX_LENGTH_STR]}'
                f'к {self.post.id} посту.'
                )


class Follow(models.Model):
    """Модель для подписки с пользователем и его подписчиком."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        """Возвращает строку подписки."""
        return (
            f'{self.user.username[:MAX_LENGTH_STR]}'
            f' подписан на {self.following.username[:MAX_LENGTH_STR]}'
        )
