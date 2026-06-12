from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.jobs_list),
    path('<int:job_pk>/', views.job_detail),
    path('fetch/', views.fetch_jobs),
    path('fetch_detail/', views.fetch_detail),
]