from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('fetch/', views.fetch_jobs),
]