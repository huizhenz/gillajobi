from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('profile/', views.profile), # 조회, 수정
]