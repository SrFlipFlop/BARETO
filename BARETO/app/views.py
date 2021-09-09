from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.models import *
from app.serializers import *
from app.forms import *

def index(request):
    return render(request, "app/dashboard.html", {})

def max_risk(vulns):
    risks = ('Informative', 'Low', 'Medium', 'High', 'Critical')
    index = max([risks.index(v.risk) for k, v in vulns.iteritems()])
    return risks[index]

# PROJECTS
def projects(request):
    """projects = {}
    for project in Project.objects.all():        
        for asset in Asset.objects.filter(project=project.id):
            vulns = {}
            for vuln in asset.vulnerabilities.all():
                vulns.update({vuln.id : vuln})
            
            projects.update({project.id: {'info': project, 'risk': max_risk(vulns), 'issues': len(vulns)}})"""
    return render(request, "app/projects.html", {'form': ProjectForm})

def projects_data(request):
    datatables = request.GET
    draw = int(datatables.get('draw'))
    start = int(datatables.get('start'))
    length = int(datatables.get('length'))
    search = datatables.get('search[value]')
    order_col = datatables.get('order[0][column]')
    order_type = datatables.get('order[0][dir]', 'asc')

    projects = Project.objects.all()
    records_total = projects.count()
    records_filtered = projects.count()

    if search:
        projects = Project.objects.filter(
                Q(name__icontains=search)|
                Q(program_name__icontains=search)|
                Q(state__icontains=search)|
                Q(offers_bounties__icontains=search)
            )
        records_total = projects.count()
        records_filtered = records_total

    if order_col:
        col_type = {'asc': '', 'desc': '-'}
        if order_col == '2':
            projects = projects.annotate(num_assets=Count('asset')).order_by('{}num_assets'.format(col_type[order_type]))
        else:
            col_relatons = {'0': 'name', '1': 'program_name', '3': 'state', '4': 'offers_bounties', '5': 'max_ammount'}
            projects = projects.order_by('{}{}'.format(col_type[order_type], col_relatons[order_col]))

    paginator = Paginator(projects, length)
    try:
        object_list = paginator.page(draw).object_list
    except PageNotAnInteger:
        object_list = paginator.page(draw).object_list
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages).object_list

    data = [
        {
            'first': {'name': projects.name, 'url': projects.url},
            'source': projects.program_name,
            'assets': projects.asset_set.count(),
            'state': projects.state,
            'bounties': projects.offers_bounties,
            'max': projects.max_ammount,
        } for projects in object_list
    ]
    return JsonResponse({'draw': draw, 'recordsTotal': records_total, 'recordsFiltered': records_filtered, 'data': data})

def project_add(request):
    return render(request, "project_add.html", {})

def project_mod(request, project):
    return render(request, "project_mod.html", {})

def project_del(request, project):
    project = Project.objects.get(id=project)
    if project:
        project.delete()
    return redirect('/projects/')

def project_info(request, project):
    context = {
        'project': Project.objects.get(id=project)
    }
    return render(request, "project_info.html", context)

def project_asset(request, project):
    context = {
        'project': Project.objects.get(id=project),
        'assets' : Asset.objects.filter(project=project)
    }
    return render(request, "project_asset.html", context)

def project_vuln(request, project):
    assets = Asset.objects.filter(project=project)
    vulns = []
    for asset in assets:
        for vuln in asset.vulnerabilities.all():
            vulns.append(vuln)

    context = {
        'project': Project.objects.get(id=project),
        'assets': assets,
        'vulnerabilities': vulns,
    }
    return render(request, "project_vuln.html", context)

# ASSETS
def asset_add(request, project):
    return redirect('/project/{0}/'.format(project))

def asset_mod(request, project):
    return redirect('/project/{0}/'.format(project))

def asset_del(request, project):
    return redirect('/project/{0}/'.format(project))

# VULNERABILITIES
def vuln_add(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_mod(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_del(request, project):
    return redirect('/project/{0}/'.format(project))

# API
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer