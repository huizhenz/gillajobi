from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]

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

    birth = models.DateField()

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

    education = models.TextField(
        blank=True,
        null=True
    )

    certification = models.TextField(
        blank=True,
        null=True
    )

    experience = models.TextField(
        blank=True,
        null=True
    )

    language = models.TextField(
        blank=True,
        null=True
    )

    preferred_location = models.TextField(
        blank=True,
        null=True
    )

    preferred_position = models.TextField(
        blank=True,
        null=True
    )

    desired_salary = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'