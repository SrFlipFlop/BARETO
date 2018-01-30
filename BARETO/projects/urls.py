from django.conf.urls import url

from projects.views import *

urlpatterns = [
    url(r'^$', ProjectsView.as_view(), name='projects'),
]