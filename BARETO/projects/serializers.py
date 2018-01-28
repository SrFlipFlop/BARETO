# -*- coding: utf-8 -*-
from rest_framework import serializers

from models import Project, Asset, Vulnerability

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'status', 'start', 'finished', 'notes')

class VulnerabilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ('id', 'name', 'risk', 'cvss', 'category', 'status', 'description', 'impact', 'recomendation') 

class AssetSerializer(serializers.HyperlinkedModelSerializer):
    #vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)
    vulnerabilities = VulnerabilitySerializer(many=True)

    class Meta:
        model = Asset
        fields = ('id', 'name', 'notes', 'project', 'vulnerabilities')