from django.conf.urls import url

from projects.views import *

urlpatterns = [
	url(r'^project/(?P<project>[\d]+)$', project, name='project'),
    url(r'^$', projects, name='projects'),
]