from django.urls import path
from . import views

app_name = 'bootcamps'
urlpatterns = [
    path('', views.bootcamps_list),
    path('<int:bootcamp_pk>/', views.bootcamp_detail),
    path('fetch/', views.fetch_bootcamps),
]
