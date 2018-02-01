from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render

from projects.models import *
from projects.serializers import *

def projects(request):
    projects = Project.objects.all()
    for project in projects:
        assets = Asset.objects.find(project=project.id)
        for asset in assets:

            num_vulns = asset.vulnerabilities

    return render(request, "projects.html", {'projects' : projects})

def project(request, project):
    return render(request, "project.html", {'id':project})

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