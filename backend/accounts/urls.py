from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('signup/', views.signup),
    path('profile/create/', views.create_profile),
    path('profile/', views.profile),
    path('profile/update/', views.update_profile),
]