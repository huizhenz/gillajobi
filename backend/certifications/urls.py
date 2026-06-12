from django.urls import path
from . import views

app_name = 'certifications'
urlpatterns = [
    path('fetch/', views.fetch_certifications),
    path('sync/', views.sync_certifications),
]