# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField

PROJECT_STATUS = (
    ('C', 'On course'),
    ('P', 'Paused'),
    ('F', 'Finished'),
)

class Project(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=1, choices=PROJECT_STATUS)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    finished = models.DateTimeField(auto_now_add=True, blank=True)
    notes = HTMLField()

    def __unicode__(self):
        return self.name

class Vulnerability(models.Model):
    name = models.CharField(max_length=250)
    risk = models.CharField(max_length=250)
    cvss = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    description = HTMLField()
    impact = HTMLField()
    recomendation = HTMLField()

    def __unicode__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=250)
    notes = HTMLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vulnerabilities = models.ManyToManyField(Vulnerability, through='AssetVulnerability')
    #vulnerabilities = models.ManyToManyField(Vulnerability) 

    def __unicode__(self):
        return self.name

class AssetVulnerability(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    vulnerability = models.ForeignKey(Vulnerability)