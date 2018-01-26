# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    start = models.DateTimeField()
    finished = models.DateField()
    notes = models.TextField()

class Asset(models.Model):
    name = models.CharField(max_length=250)
    notes = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Vulnerability(models.Model):
    name = models.CharField(max_length=250)
    risk = models.CharField(max_length=250)
    cvss = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    description = models.TextField()
    impact = models.TextField()
    recomendation = models.TextField()

class AssetVulnerability(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    vulnerability = models.ForeignKey(Vulnerability)