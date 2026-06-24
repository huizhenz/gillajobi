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
        # self.embed_jobs()
        # self.embed_bootcamps()
        # self.embed_certifications()
        self.embed_competitions()

    def embed_jobs(self):
        # Recruitment DB 전체 조회 (RecruitmentDetail까지 prefetch)
        recruitments = Recruitment.objects.select_related('detail').all()
        
        for recruitment in recruitments:
            job_description = recruitment.detail.job_description
            text = f"{recruitment.title} {job_description}"

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
        

    def embed_bootcamps(self):
        # skills는 ManyToManyField라서
        bootcamps = Bootcamp.objects.prefetch_related('skills').all()

        for bootcamp in bootcamps:
            skills = " ".join([skill.name for skill in bootcamp.skills.all()])
            text = f"{bootcamp.title} {skills}"

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


    def embed_certifications(self):
        certifications = Certification.objects.all()

        for certification in certifications:
            text = f"{certification.name} {certification.major_job_field} {certification.minor_job_field}"

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


    def embed_competitions(self):
        competitions = Competition.objects.all()

        for competition in competitions:
            text = f"{competition.title} {competition.keyword}"

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