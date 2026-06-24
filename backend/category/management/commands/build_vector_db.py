import json

from django.core.management.base import BaseCommand

from category.chroma import jobs_col, bootcamps_col, certifications_col, competitions_col
from category.utils import generate_embedding

from jobs.models import Recruitment
from bootcamps.models import Bootcamp
from certifications.models import Certification
from competitions.models import Competition


class Command(BaseCommand):
    help = 'DB 데이터를 ChromaDB에 임베딩하여 저장'

    def handle(self, *args, **kwargs):
        self.embed_jobs()
        self.embed_bootcamps()
        self.embed_certifications()
        self.embed_competitions()

    def embed_jobs(self):
        # Recruitment DB 전체 조회 (RecruitmentDetail까지 prefetch)
        recruitments = Recruitment.objects.select_related('detail', 'category').all()
        
        for recruitment in recruitments:
            job_description = recruitment.detail.job_description or ''
            category_name = recruitment.category.name if recruitment.category else ''
            text = f"{recruitment.title} {job_description[:300]} {category_name}"

            # text -> embedding 생성
            embedding = generate_embedding(text)

            # embedding -> ChromaDB 저장
            jobs_col.add(
                ids=[f"job_{recruitment.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "job",
                    "id": recruitment.id,
                    "title": recruitment.title,
                }]
            )
        print('jobs 완료')
        

    def embed_bootcamps(self):
        # skills는 ManyToManyField라서
        bootcamps = Bootcamp.objects.select_related('category').prefetch_related('skills').all()

        for bootcamp in bootcamps:
            skills = " ".join([skill.name for skill in bootcamp.skills.all()])
            category_name = bootcamp.category.name if bootcamp.category else ''
            text = f"{bootcamp.title} {bootcamp.program_process} {skills} {category_name}"
            
            embedding = generate_embedding(text)

            bootcamps_col.add(
                ids=[f"bootcamp_{bootcamp.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "bootcamp",
                    "id": bootcamp.id,
                    "title": bootcamp.title,
                }]
            )
        print('bootcamps 완료')


    def embed_certifications(self):
        certifications = Certification.objects.select_related('category').all()

        for certification in certifications:
            category_name = certification.category.name if certification.category else ''
            text = f"{certification.name} {certification.major_job_field} {certification.minor_job_field} {category_name}"

            embedding = generate_embedding(text)

            certifications_col.add(
                ids=[f"certification_{certification.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "certification",
                    "id": certification.id,
                    "title": certification.name,
                }]
            )
        print('certifications 완료')


    def embed_competitions(self):
        competitions = Competition.objects.select_related('category').all()
        fields = ['공모개요', '공모주제', '응모주제', '공모분야', '공모내용']

        for competition in competitions:
            description_text = ' '.join([
                str(competition.description.get(key, '')) for key in fields
                if competition.description.get(key)
            ])
            category_name = competition.category.name if competition.category else ''
            text = f"{competition.title} {competition.keyword} {description_text} {category_name}"

            embedding = generate_embedding(text)
            
            competitions_col.add(
                ids=[f"competition_{competition.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "certification",
                    "id": competition.id,
                    "title": competition.title,
                }]
            )
        print('competitions 완료')