from django.conf.urls import url
from django.urls import path

from app.views import *

urlpatterns = [    
    #url(r'^project/(?P<project>[\d]+)/asset/mod$', asset_mod, name='asset_mod'),
    #url(r'^project/(?P<project>[\d]+)/asset/add$', asset_add, name='asset_add'),
    #url(r'^project/(?P<project>[\d]+)/asset/del$', asset_del, name='asset_del'),

    #url(r'^project/(?P<project>[\d]+)/vuln/mod$', vuln_mod, name='vuln_mod'),
    #url(r'^project/(?P<project>[\d]+)/vuln/add$', vuln_add, name='vuln_add'),
    #url(r'^project/(?P<project>[\d]+)/vuln/del$', vuln_del, name='vuln_del'),    
    
    #url(r'^project/(?P<project>[\d]+)/info/$', project_info, name='project_info'), 
    #url(r'^project/(?P<project>[\d]+)/asset/$', project_asset, name='project_asset'),  
    #url(r'^project/(?P<project>[\d]+)/vuln/$', project_vuln, name='project_vuln'),
    #url(r'^project/(?P<project>[\d]+)/mod$', project_mod, name='project_mod'),    
    #url(r'^project/(?P<project>[\d]+)/del$', project_del, name='project_del'),
    #url(r'^project/add$', project_add, name='project_add'),
    #url(r'^$', projects, name='projects'),

    path('', index, name='dashboard'),

    path('projects/', projects, name='projects'),
    path('projects/data/', projects_data, name='projects_data'),
    path('project/add', project_add, name='project_add'),
    path('project/<int:project>/mod', project_mod, name='project_mod'),
    path('project/<int:project>/del', project_del, name='project_del'),
    path('project/<int:project>/', project_info, name='project_info'),
    path('project/<int:project>/info/', project_info, name='project_info'),
    path('project/<int:project>/assets/', project_asset, name='project_asset'),
    path('project/<int:project>/vulns/', project_vuln, name='project_vuln'),
]