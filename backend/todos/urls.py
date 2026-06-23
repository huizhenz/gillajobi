from django.urls import path
from . import views

app_name = "todos"
urlpatterns = [
    path('', views.todo_list),
    path('<int:todo_pk>/', views.todo_detail),
]