from django.db import models
from category.models import Category, Label
from jobs.models import Company


# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Bootcamp(models.Model):
    title = models.CharField(max_length=200)

    label = models.ForeignKey(
        Label,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='labels'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bootcamps'
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bootcamps'
    )

    region = models.ForeignKey(
        'Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    program_process = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    expense = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    period = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    participation_time = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    recruitment_linkage = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    close_date = models.DateField(
        blank=True,
        null=True,
    )

    close_date_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    recruitment_url = models.URLField(
        unique=True
    )

    skills = models.ManyToManyField(
        Skill,
        related_name='bootcamps',
        blank=True
    )

    ai_fit_score = models.IntegerField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
