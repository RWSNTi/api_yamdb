from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

CHOICES = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin')
)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('Обязательное поле, только цифры, буквы или @/./+/-/_.'
                   ),
        validators=[username_validator],
        error_messages={
            'unique': ("Пользователь с этим именем уже существует."),
        },
    )
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    role = models.CharField(max_length=16, choices=CHOICES, default=CHOICES[0])
    password = models.CharField('password', max_length=25)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class RegistrationEmail(models.Model):
    email = models.EmailField('email address', unique=True)
    confirmation_code = models.CharField(max_length=10)
