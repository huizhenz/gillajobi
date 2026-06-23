from django.db import models
from django.conf import settings
from category.models import Label

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    label = models.ForeignKey(
        Label,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='todos'
    )
    todo = models.CharField(max_length=100)
    memo = models.CharField(max_length=200, blank=True, default='')
    is_completed = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    recommendation_score = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # start_date = models.DateField()
    # end_date = models.DateField()