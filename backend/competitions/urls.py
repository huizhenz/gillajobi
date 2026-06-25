from django.urls import path
from . import views

app_name = "competitions"
urlpatterns = [
    path('top3/', views.competitions_top3),
    path('fetch/', views.fetch_competitions),
    path('sync/', views.sync_competitions),
    path('fetch/detail/<int:pk>/', views.fetch_competition_detail),
]