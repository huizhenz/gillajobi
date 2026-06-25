from django.urls import path
from . import views

app_name = 'certifications'
urlpatterns = [
    path('top3/', views.certifications_top3),
    path('fetch/', views.fetch_certifications),
    path('sync/', views.sync_certifications),
    path('fetch/exam/', views.fetch_examinations),
    path('sync/exam/', views.sync_examinations),
    path('fetch/detail/<str:jm_cd>/', views.fetch_certification_detail)
]
