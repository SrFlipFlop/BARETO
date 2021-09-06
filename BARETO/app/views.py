from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render, redirect

from app.models import *
from app.serializers import *

def projects(request):
    projects = {}
    for project in Project.objects.all():        
        for asset in Asset.objects.filter(project=project.id):
            vulns = {}
            for vuln in asset.vulnerabilities.all():
                vulns.update({vuln.id : vuln})
            
            projects.update({project.id: {'info': project, 'risk': max_risk(vulns), 'issues': len(vulns)}})

    return render(request, "projects.html", {'projects' : projects})

def max_risk(vulns):
    risks = ('Informative', 'Low', 'Medium', 'High', 'Critical')
    index = max([risks.index(v.risk) for k, v in vulns.iteritems()])
    return risks[index]

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

def asset_add(request, project):
    return redirect('/project/{0}/'.format(project))

def asset_mod(request, project):
    return redirect('/project/{0}/'.format(project))

def asset_del(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_add(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_mod(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_del(request, project):
    return redirect('/project/{0}/'.format(project))

# === API views
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer