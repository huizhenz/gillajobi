from django.db import models
from category.models import Category

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    industry = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=100, blank=True)

    established_year = models.IntegerField(
        blank=True,
        null=True,
    )

    annual_sales = models.CharField(
        max_length=255,
        blank=True,
    )

    employee_count = models.IntegerField(
        blank=True,
        null=True,
    )

    homepage = models.URLField(
        blank=True,
        null=True,
    )

    logo_url = models.URLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

class Recruitment(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='recruitments'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='recruitments',
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=255)

    career = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    education = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    salary = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    employment_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    working_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    recruitment_count = models.IntegerField(
        blank=True,
        null=True,
    )

    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    recruitment_url = models.URLField(unique=True)

    close_date = models.DateField(
        blank=True,
        null=True,
    )

    created_date = models.DateField(
        blank=True,
        null=True,
    )

    view_count = models.IntegerField(
        blank=True,
        null=True,
    )

    wanted_auth_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class RecruitmentDetail(models.Model):

    recruitment = models.OneToOneField(
        Recruitment,
        on_delete=models.CASCADE,
        related_name='detail'
    )

    job_description = models.TextField(
        blank=True,
        null=True
    )

    qualification = models.TextField(
        blank=True,
        null=True
    )

    preferred_qualification = models.TextField(
        blank=True,
        null=True
    )

    license = models.TextField(
        blank=True,
        null=True
    )

    computer_skill = models.TextField(
        blank=True,
        null=True
    )

    foreign_language = models.TextField(
        blank=True,
        null=True
    )

    working_hours = models.TextField(
        blank=True,
        null=True
    )

    break_time = models.TextField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    social_insurance = models.TextField(
        blank=True,
        null=True
    )

    retirement_pay = models.TextField(
        blank=True,
        null=True
    )

    submission_documents = models.TextField(
        blank=True,
        null=True
    )

    application_method = models.TextField(
        blank=True,
        null=True
    )

class HiringProcess(models.Model):

    recruitment = models.ForeignKey(
        Recruitment,
        on_delete=models.CASCADE,
        related_name='processes'
    )

    name = models.CharField(max_length=100)

    class Meta:
        unique_together = [('recruitment', 'name')]