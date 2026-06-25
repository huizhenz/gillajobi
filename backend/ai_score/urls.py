from django.urls import path
from . import views

app_name = 'ai_scores'
urlpatterns = [
    path('recommendations/', views.recommendations),
    path('score/', views.single_score),
]
