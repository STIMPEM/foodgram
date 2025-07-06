from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from constants import (
    USER_EMAIL_MAX_LENGTH,
    USER_FIRST_NAME_MAX_LENGTH,
    USER_LAST_NAME_MAX_LENGTH,
    USER_USERNAME_MAX_LENGTH,
)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=USER_EMAIL_MAX_LENGTH
    )

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=USER_USERNAME_MAX_LENGTH,
        unique=True,
        help_text=(
            'Обязательное поле. Не более 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_'
        ),
        validators=[username_validator],
        error_messages={
            'unique': (
                'Пользователь с таким именем пользователя '
                'уже существует'
            )
        }
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_FIRST_NAME_MAX_LENGTH
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_LAST_NAME_MAX_LENGTH
    )

    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='Загрузите ваш аватар'
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    subscription_date = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-subscription_date']
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_user_author_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='prevent_self_subscription'
            )
        ]

    def __str__(self):
        return f'{self.subscriber.username} подписан на {self.author.username}'