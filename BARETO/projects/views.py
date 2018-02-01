from __future__ import unicode_literals

from rest_framework import viewsets

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

from projects.models import *
from projects.serializers import *

class ProjectsView(ListView):
    model = Project
    template_name = "projects.html"

class ProjectView(TemplateView):
	template_name = "project.html"

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer