# Generated by Django 3.0.5 on 2021-09-06 20:43

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('notes', tinymce.models.HTMLField(default='TBC')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('On course', 'On course'), ('Paused', 'Paused'), ('Finished', 'Finished')], max_length=50)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('finished', models.DateTimeField(auto_now_add=True)),
                ('notes', tinymce.models.HTMLField(default='TBC')),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('risk', models.CharField(choices=[('Critical', 'Critical'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low'), ('Informative', 'Informative')], max_length=50)),
                ('cvss', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Ready', 'Ready'), ('Finished', 'Finished')], max_length=50)),
                ('description', tinymce.models.HTMLField(default='TBC')),
                ('impact', tinymce.models.HTMLField(default='TBC')),
                ('recomendation', tinymce.models.HTMLField(default='TBC')),
            ],
        ),
        migrations.CreateModel(
            name='AssetVulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Asset')),
                ('vulnerability', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Vulnerability')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Project'),
        ),
        migrations.AddField(
            model_name='asset',
            name='vulnerabilities',
            field=models.ManyToManyField(through='app.AssetVulnerability', to='app.Vulnerability'),
        ),
    ]
