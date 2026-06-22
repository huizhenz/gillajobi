from django.urls import path
from . import views

app_name = 'bootcamps'
urlpatterns = [
    path('', views.bootcamps_list),
    path('fetch/', views.fetch_bootcamps),
]
