from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from app.views import ProjectViewSet, AssetViewSet, VulnerabilityViewSet, TemplateViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='Project')
router.register(r'assets', AssetViewSet, basename='Asset')
router.register(r'vulnerabilities', VulnerabilityViewSet, basename='Vulnerability')
router.register(r'templates', TemplateViewSet, basename='Template')

urlpatterns = [    
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('app.urls')),
]
