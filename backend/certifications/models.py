from django.db import models

class Certification(models.Model):
    jm_cd = models.CharField(max_length=20, unique=True) # 종목코드
    name = models.CharField(max_length=200, blank=True, null=True) # 종목명
    qualification_cl = models.CharField(max_length=50, blank=True, null=True) # 국가기술자격
    # grade = models.CharField(max_length=50, blank=True) # 등급명
    # institution = models.CharField(max_length=100, blank=True) # 시행기관명
    series_name = models.CharField(max_length=100, blank=True, null=True) # 계열명 (기사, 산업기사, 기능사 등)
    major_job_field = models.CharField(max_length=100, blank=True, null=True) # 직무분야 대분류
    minor_job_field = models.CharField(max_length=100, blank=True, null=True) # 직무분야 중분류
    ai_score = models.IntegerField(blank=True, null=True) # AI 분석 점수

    # def __str__(self):
    #     return f"{self.name} ({self.qualification_cl})"