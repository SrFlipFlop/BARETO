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
    path('project/<uuid:project>/', project_info, name='project_info'),
    path('project/<uuid:project>/del', project_del, name='project_del'),
    
    path('project/<uuid:project>/assets/', project_asset, name='project_asset'),
    path('project/<uuid:project>/assets/data/', assets_data, name='assets_data'),
    path('project/<uuid:project>/assets/add', asset_add, name='asset_add'),
    path('project/<uuid:project>/assets/<uuid:asset>/', asset_mod, name='asset_mod'),
    path('project/<uuid:project>/assets/<uuid:asset>/del', asset_del, name='asset_del'),

    path('project/<uuid:project>/vulns/', project_vuln, name='project_vuln'),
    path('project/<uuid:project>/vulns/data/', vulns_data, name='vulns_data'),
    path('project/<uuid:project>/vulns/add', vuln_add, name='vuln_add'),
    path('project/<uuid:project>/vulns/<uuid:vuln>/', vuln_mod, name='vuln_mod'),
    path('project/<uuid:project>/vulns/<uuid:vuln>/del', vuln_del, name='vuln_del'),

    path('assets/', assets, name='assets'),

    path('clients/', clients, name='clients'),
    path('clients/groups/add', clients_add_group, name='clients_add_group'),
    path('clients/groups/<int:group>/mod', clients_mod_group, name='clients_mod_group'),
    path('clients/groups/<int:group>/del', clients_del_group, name='clients_del_group'),
    path('clients/users/add', clients_add_user, name='clients_add_user'),
    path('clients/users/<int:user>/mod', clients_mod_user, name='clients_mod_user'),
    path('clients/users/<int:user>/del', clients_del_user, name='clients_del_user'),
]