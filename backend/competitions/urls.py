from django.urls import path
from . import views

app_name = "competitions"
urlpatterns = [
    path('fetch/', views.fetch_competitions),
    path('sync/', views.sync_competitions),
]