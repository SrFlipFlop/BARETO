from django.contrib import admin
from . import models

admin.site.register(models.Project)
admin.site.register(models.Vulnerability)
admin.site.register(models.Template)
admin.site.register(models.Asset)