# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuid import uuid4
from django.db import models
from django.contrib.auth.models import Group
from tinymce.models import HTMLField

PROJECT_STATUS = (
    (1, 'Planning'),
    (2, 'On course'),
    (3, 'Paused'),
    (4, 'Finished'),
)

ASSET_TYPE = (
    (1, 'Web'),
    (2, 'Infrastructure'),
    (3, 'Android application'),
    (4, 'iOS application'),
    (5, 'Code'),
    (6, 'IoT'),
    (7, 'Other'),
)

VULNERABILITY_STATUS = (
    (1, 'Draft'),
    (2, 'Ready'),
    (3, 'Finished'),
)

VULNERABILITY_RISK = (
    (1, 'Informative'),
    (2, 'Low'),
    (3, 'Medium'),
    (4, 'High'),
    (5, 'Critical')
)

VULNERABILITY_TYPE = (
    (1, 'Other'),
)

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    status = models.IntegerField(choices=PROJECT_STATUS, default=1)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    finished = models.DateTimeField(auto_now_add=True, blank=True)
    client = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    notes = HTMLField(default='TBC')

    def __str__(self):
        return self.name

class Vulnerability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    risk = models.IntegerField(choices=VULNERABILITY_RISK, default=1)
    cvss = models.CharField(max_length=250)
    status = models.IntegerField(choices=VULNERABILITY_STATUS, default=1)
    type = models.IntegerField(choices=VULNERABILITY_TYPE, default=1)
    description = HTMLField(default='TBC')
    impact = HTMLField(default='TBC')
    recomendation = HTMLField(default='TBC')

    def __str__(self):
        return self.name

class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    risk = models.IntegerField(choices=VULNERABILITY_RISK, default=1)
    cvss = models.CharField(max_length=250)
    status = models.IntegerField(choices=VULNERABILITY_STATUS, default=1)
    type = models.IntegerField(choices=VULNERABILITY_TYPE, default=1)
    description = HTMLField(default='TBC')
    impact = HTMLField(default='TBC')
    recomendation = HTMLField(default='TBC')

    def __str__(self):
        return self.name

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=250)
    type = models.IntegerField(choices=ASSET_TYPE, default=1)
    notes = HTMLField(default='TBC')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vulnerabilities = models.ManyToManyField(Vulnerability)

    def __str__(self):
        return self.name