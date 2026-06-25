from django.db import models
from category.models import Category, Label

class Certification(models.Model):
    label = models.ForeignKey(
        Label,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certifications'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certifications'
    )
    jm_cd = models.CharField(max_length=20, unique=True) # 종목코드
    name = models.CharField(max_length=200, blank=True) # 종목명
    qualification_cl = models.CharField(max_length=50, blank=True) # 국가기술자격
    series_name = models.CharField(max_length=100, blank=True) # 계열명 (기사, 산업기사, 기능사 등)
    major_job_field = models.CharField(max_length=100, blank=True) # 직무분야 대분류
    minor_job_field = models.CharField(max_length=100, blank=True) # 직무분야 중분류

    view_count = models.IntegerField(default=0)


class Examination(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='examinations', to_field='jm_cd')
    # jm_cd = models.CharField(max_length=10, unique=True) # 종목코드 (요청 파라미터)
    jm_name = models.CharField(max_length=100) # 종목명
    plan_name = models.CharField(max_length=200) # 회차명

    # 필기
    doc_reg_start = models.DateField(blank=True, null=True) # 필기시험 원서접수 시작일자
    doc_reg_end = models.DateField(blank=True, null=True) # 필기시험 원서접수 종료일자
    doc_exam_start = models.DateField(blank=True, null=True) # 필기시험 시작일자
    doc_exam_end = models.DateField(blank=True, null=True) # 필기시험 종료일자
    doc_pass_dt = models.DateField(blank=True, null=True) # 필기시험 합격(예정)자 발표일자
    doc_submit_start = models.DateField(blank=True, null=True) # 응시자격 서류제출 시작일자
    doc_submit_end = models.DateField(blank=True, null=True) # 응시자격 서류제출 종료일자

    # 실기
    prac_reg_start = models.DateField(blank=True, null=True) # 실기시험 원서접수 시작일자
    prac_reg_end = models.DateField(blank=True, null=True) # 실기시험 원서접수 종료일자
    prac_exam_start = models.DateField(blank=True, null=True) # 실기시험 시작일자
    prac_exam_end = models.DateField(blank=True, null=True) # 실기시험 종료일자
    prac_pass_start = models.DateField(blank=True, null=True) # 합격자발표 시작일자
    prac_pass_end = models.DateField(blank=True, null=True) # 합격자발표 종료일자

    class Meta:
        unique_together = ('certification', 'plan_name')