# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Projects(models.Model):
    project_name = models.CharField(max_length=250)
    project_status = models.CharField(max_length=250)
    project_start = models.DateTimeField()
    project_finished = models.DateField()
    project_notes = models.TextField()

class Assets(models.Model):
    asset_name = models.CharField(max_length=250)
    asset_notes = models.TextField()
    asset_project = models.ForeignKey(Projects, on_delete=models.CASCADE)

class Vulnerabilities(models.Model):
    vuln_name = models.CharField(max_length=250)
