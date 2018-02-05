# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField

PROJECT_STATUS = (
    ('On course', 'On course'),
    ('Paused', 'Paused'),
    ('Finished', 'Finished'),
)

VULNERABILITY_STATUS = (
    ('Draft', 'Draft'),
    ('Ready', 'Ready'),
    ('Finished', 'Finished'),
)

VULNERABILITY_RISK = (
    ('Critical', 'Critical'),
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
    ('Informative', 'Informative')
)

class Project(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=PROJECT_STATUS)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    finished = models.DateTimeField(auto_now_add=True, blank=True)
    notes = HTMLField(default='TBC')

    def __unicode__(self):
        return self.name

class Vulnerability(models.Model):
    name = models.CharField(max_length=250)
    risk = models.CharField(max_length=50, choices=VULNERABILITY_RISK)
    cvss = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=VULNERABILITY_STATUS)
    description = HTMLField(default='TBC')
    impact = HTMLField(default='TBC')
    recomendation = HTMLField(default='TBC')

    def __unicode__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=250)
    notes = HTMLField(default='TBC')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vulnerabilities = models.ManyToManyField(Vulnerability, through='AssetVulnerability')

    def __unicode__(self):
        return self.name

class AssetVulnerability(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    vulnerability = models.ForeignKey(Vulnerability)