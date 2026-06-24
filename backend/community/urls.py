from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('labels/', views.label_list),
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.comment_list_create),
    path('comments/<int:comment_pk>/', views.comment_delete),
]