"""
URL configuration for gillajobi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/ai_score/', include('ai_score.urls')),
    path('api/v1/bootcamps/', include('bootcamps.urls')),
    path('api/v1/certifications/', include('certifications.urls')),
    path('api/v1/community/', include('community.urls')),
    path('api/v1/competitions/', include('competitions.urls')),
    path('api/v1/jobs/', include('jobs.urls')),
    path('api/v1/todos/', include('todos.urls')),
    path('api/v1/category/', include('category.urls')),

    # Swagger (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)