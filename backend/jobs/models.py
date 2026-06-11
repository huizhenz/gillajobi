from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    homepage = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Recruitment(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='recruitments',
    )

    category = models.ForeignKey(
        'category.Category',
        on_delete=models.SET_NULL,
        related_name='recruitments',
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    industry_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    salary = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    working_hours = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    personal_history = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    education = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    close_date = models.DateField(
        blank=True,
        null=True,
    )

    employment_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    personnel = models.IntegerField(
        blank=True,
        null=True,
    )

    recruitment_url = models.URLField(
        blank=True,
        null=True,
    )

    ai_recommend_score = models.FloatField(
        default=0,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title


class RecruitmentDetail(models.Model):
    recruitment = models.OneToOneField(
        Recruitment,
        on_delete=models.CASCADE,
        related_name='detail',
    )

    job_description = models.TextField(
        blank=True,
        null=True,
    )

    qualification = models.TextField(
        blank=True,
        null=True,
    )

    preferred_qualification = models.TextField(
        blank=True,
        null=True,
    )

    benefits = models.TextField(
        blank=True,
        null=True,
    )

    hiring_process = models.TextField(
        blank=True,
        null=True,
    )

    basic_address = models.TextField(
        blank=True,
        null=True,
    )

    company_intro = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'{self.recruitment.title} 상세정보'