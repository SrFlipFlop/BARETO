# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Project, Asset, Vulnerability

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','name', 'status', 'start', 'finished', 'notes', 'client']

    def create(self, data):
        groups = self.context['request'].user.groups.all()
        if not groups.filter(id=data['client'].id).exists():
            raise serializers.ValidationError('403 Forbidden')    
        return Project.objects.create(**data)

class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = ('id', 'name', 'risk', 'cvss', 'type', 'status', 'description', 'impact', 'recomendation')

class VulnerabilityListSerializer(serializers.ListSerializer):
    #child = VulnerabilitySerializer()

    class Meta:
        model = Vulnerability
        fields = ('id',)

class AssetSerializer(serializers.ModelSerializer):
    vulnerabilities = VulnerabilityListSerializer#(many=True) #TODO: error

    class Meta:
        model = Asset
        fields = ('id', 'name', 'notes', 'project', 'vulnerabilities')
        #read_only_fields = ('vulnerabilities',) #TODO: allow create Asset without vulnerabilities

    def create(self, data):
        groups = self.context['request'].user.groups.all()   
        if not groups.filter(id=data['project'].client.id).exists():
            raise serializers.ValidationError('403 Forbidden')
        return Asset.objects.create(**data)