from django.db import models
from category.models import Category, Label

# Create your models here.
class Competition(models.Model):
    label = models.ForeignKey(
        Label,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='competitions'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='competitions'
    )
    external_id = models.IntegerField(unique=True)  # 씽유 공모전 고유 ID
    title = models.CharField(max_length=255) # 공모전 제목
    host = models.CharField(max_length=255) # 주최사
    start_date = models.DateField(null=True, blank=True) # 접수 시작일
    end_date = models.DateField(null=True, blank=True) # 접수 종료일
    keyword = models.CharField(max_length=100, blank=True) # 응모 분야 (아이디어/마케팅 등)
    homepage = models.URLField(blank=True) # 공모전 공식 홈페이지 URL
    thumbnail = models.URLField(blank=True) # 썸네일 이미지 URL
    detail_url = models.URLField(blank=True) # 상세 페이지 URL
    description = models.JSONField(default=dict) # 공모 요강 (페이지마다 다른 항목)