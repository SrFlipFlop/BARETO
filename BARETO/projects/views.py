from __future__ import unicode_literals
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse

from models import *
from serializers import *

def index(request):
    return render(request, 'projects/index.html', {})

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer