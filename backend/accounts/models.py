from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]

# dj-rest-auth 사용, 추가 컬럼만 지정

class User(AbstractUser):
    nickname = models.CharField(
        max_length=125,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )

    birth = models.DateField(
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    education = models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    certification = models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    experience = models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    language = models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    preferred_location = models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    preferred_position = models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    desired_salary = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'
