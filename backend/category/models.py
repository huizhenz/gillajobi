from django.db import models

# Create your models here.
class Category(models.Model): #21개 - it, marketing
    name = models.CharField(max_length=100)

class Label(models.Model): #4개 - job, bootcamp
    name = models.CharField(max_length=100)