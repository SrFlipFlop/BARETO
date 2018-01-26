from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^projects/', include('projects.urls')),
    #url(r'^admin/', admin.site.urls),
]
