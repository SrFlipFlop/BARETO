from django.conf.urls import url

from projects.views import *

urlpatterns = [
	url(r'^project/$', ProjectView.as_view(), name='project'),
    url(r'^$', ProjectsView.as_view(), name='projects'),
]