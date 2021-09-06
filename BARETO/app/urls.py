from django.conf.urls import url

from app.views import *

urlpatterns = [    
    url(r'^project/(?P<project>[\d]+)/asset/mod$', asset_mod, name='asset_mod'),
    url(r'^project/(?P<project>[\d]+)/asset/add$', asset_add, name='asset_add'),
    url(r'^project/(?P<project>[\d]+)/asset/del$', asset_del, name='asset_del'),

    url(r'^project/(?P<project>[\d]+)/vuln/mod$', vuln_mod, name='vuln_mod'),
    url(r'^project/(?P<project>[\d]+)/vuln/add$', vuln_add, name='vuln_add'),
    url(r'^project/(?P<project>[\d]+)/vuln/del$', vuln_del, name='vuln_del'),    
    
    url(r'^project/(?P<project>[\d]+)/info/$', project_info, name='project_info'), 
    url(r'^project/(?P<project>[\d]+)/asset/$', project_asset, name='project_asset'),  
    url(r'^project/(?P<project>[\d]+)/vuln/$', project_vuln, name='project_vuln'),
    url(r'^project/(?P<project>[\d]+)/$', project_info, name='project'),

    url(r'^$', projects, name='projects'),
]