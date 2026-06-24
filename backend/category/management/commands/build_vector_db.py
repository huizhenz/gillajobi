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
        recruitments = Recruitment.objects.select_related('detail', 'category', 'label').all()

        for i, recruitment in enumerate(recruitments, 1):
            detail = getattr(recruitment, 'detail', None)
            qualification = (detail.qualification or '') if detail else ''
            preferred_qualification = (detail.preferred_qualification or '') if detail else ''
            category_name = recruitment.category.name if recruitment.category else ''
            label_name = recruitment.label.name if recruitment.label else ''

            text = f"{recruitment.title} {label_name} {category_name} {qualification[:300]} {preferred_qualification[:200]}"

            embedding = generate_embedding(text)

            jobs_col.upsert(
                ids=[f"job_{recruitment.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "job",
                    "id": recruitment.id,
                    "title": recruitment.title,
                    "label_name": label_name,
                }]
            )
            if i % 100 == 0:
                print(f'jobs {i}개 처리 중...')
        print('jobs 완료')
        

    def embed_bootcamps(self):
        bootcamps = Bootcamp.objects.select_related('category', 'label').prefetch_related('skills').all()

        for bootcamp in bootcamps:
            skills = " ".join([skill.name for skill in bootcamp.skills.all()])
            category_name = bootcamp.category.name if bootcamp.category else ''
            label_name = bootcamp.label.name if bootcamp.label else ''
            text = f"{bootcamp.title} {label_name} {bootcamp.program_process} {skills} {category_name}"

            embedding = generate_embedding(text)

            bootcamps_col.upsert(
                ids=[f"bootcamp_{bootcamp.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "bootcamp",
                    "id": bootcamp.id,
                    "title": bootcamp.title,
                    "label_name": label_name,
                }]
            )
        print('bootcamps 완료')


    def embed_certifications(self):
        certifications = Certification.objects.select_related('category', 'label').all()

        for certification in certifications:
            category_name = certification.category.name if certification.category else ''
            label_name = certification.label.name if certification.label else ''
            text = f"{certification.name} {label_name} {certification.major_job_field} {certification.minor_job_field} {category_name}"

            embedding = generate_embedding(text)

            certifications_col.upsert(
                ids=[f"certification_{certification.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "certification",
                    "id": certification.id,
                    "title": certification.name,
                    "label_name": label_name,
                }]
            )
        print('certifications 완료')


    def embed_competitions(self):
        competitions = Competition.objects.select_related('category', 'label').all()
        fields = ['공모개요', '공모주제', '응모주제', '공모분야', '공모내용']

        for competition in competitions:
            description_text = ' '.join([
                str(competition.description.get(key, '')) for key in fields
                if competition.description.get(key)
            ])
            category_name = competition.category.name if competition.category else ''
            label_name = competition.label.name if competition.label else ''
            text = f"{competition.title} {label_name} {competition.keyword} {description_text} {category_name}"

            embedding = generate_embedding(text)

            competitions_col.upsert(
                ids=[f"competition_{competition.id}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "competition",
                    "id": competition.id,
                    "title": competition.title,
                    "label_name": label_name,
                }]
            )
        print('competitions 완료')