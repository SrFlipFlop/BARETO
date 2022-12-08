from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from app.views import ProjectViewSet, AssetViewSet, VulnerabilityViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'vulnerabilities', VulnerabilityViewSet)

urlpatterns = [    
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('app.urls')),
]
