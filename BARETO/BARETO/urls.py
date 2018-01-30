from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from projects.views import ProjectViewSet, AssetViewSet, VulnerabilityViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'vulnerabilities', VulnerabilityViewSet)

urlpatterns = [    
    url(r'^api/', include(router.urls)),
    #url(r'^admin/', admin.site.urls),
    #url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('projects.urls')),
]
