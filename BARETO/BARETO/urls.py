from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from app.views import ProjectViewSet, AssetViewSet, VulnerabilityViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'vulnerabilities', VulnerabilityViewSet)

urlpatterns = [    
    path(r'api/', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'tinymce/', include('tinymce.urls')),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'', include('app.urls')),
]
