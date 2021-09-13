from __future__ import unicode_literals

from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group

from app.models import *
from app.serializers import *
from app.forms import *

def index(request):
    return render(request, "app/dashboard.html", {})

def max_risk(vulns):
    risks = ('Informative', 'Low', 'Medium', 'High', 'Critical')
    index = max([risks.index(v.risk) for k, v in vulns.iteritems()])
    return risks[index]

# CLIENTS
def clients(request):
    users = []
    for user in User.objects.all():
        users.append({
            'id': user.pk,
            'name': user.username,
            'clients': ', '.join([g.name for g in user.groups.all()]),
        })
    
    clients = []
    for group in Group.objects.all():
        clients.append({
            'id': group.pk,
            'name': group.name,
            'projects': Project.objects.filter(client__name=group.name).count(),
            'users': User.objects.filter(groups__name=group.name).count(),
        })
    return render(request, "app/clients.html", {'users': users, 'clients': clients, 'form': UserClientCreateForm})

def clients_add_group(request):
    if request.method == 'POST':
        new_group, created = Group.objects.get_or_create(name=request.POST.get('clientName', 'Default'))
    return redirect('clients')

def clients_mod_group(request, group):
    if request.user.is_superuser:
        instance = get_object_or_404(Group, pk=group)
        if request.method == 'GET':
            return render(request, "app/client_mod.html", {'current': instance})
        else:
            new_name = request.POST.get('clientName')
            if not Group.objects.filter(name=new_name):
                instance.name = new_name
                instance.save()

    return redirect('clients')

def clients_del_group(request, group):
    if request.user.is_superuser:
        group = get_object_or_404(Group, pk=group)
        group.delete()
    return redirect('clients')

def clients_add_user(request):
    if request.method == 'POST':
        form = UserClientCreateForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password1'])
            for group in form.cleaned_data['groups']:
                new_user.groups.add(group)
            new_user.save()

    return redirect('clients')

def clients_mod_user(request, user):
    if request.user.is_superuser:
        user = get_object_or_404(User, pk=user)
        form = UserClientUpdateForm(request.POST or None, instance=user)
        if not form.is_valid():
            return render(request, "app/user_mod.html", {'current': user, 'form': form})
        
        user = form.save()
        for group in form.cleaned_data.get('groups'):
            user.groups.add(group)
        user.save()
    return redirect('clients')

def clients_del_user(request, user):
    if request.user.is_superuser:
        user = get_object_or_404(User, pk=user)
        user.delete()
    return redirect('clients')

# PROJECTS
def projects(request):  
    form = ProjectForm(user=request.user)
    return render(request, "app/projects.html", {'form': form})

def projects_data(request):
    datatables = request.GET
    draw = int(datatables.get('draw'))
    start = int(datatables.get('start'))
    length = int(datatables.get('length'))
    search = datatables.get('search[value]')
    order_col = datatables.get('order[0][column]')
    order_type = datatables.get('order[0][dir]', 'asc')

    projects = Project.objects.filter(client__in=request.user.groups.all())
    records_total = projects.count()
    records_filtered = projects.count()

    if search:
        projects = projects.filter(
                Q(name__icontains=search)|
                Q(status__icontains=search)|
                Q(start__icontains=search)|
                Q(finished__icontains=search)
            )
        records_total = projects.count()
        records_filtered = records_total

    #if order_col:
    #    col_type = {'asc': '', 'desc': '-'}
    #    if order_col == '2':
    #        projects = projects.annotate(num_assets=Count('asset')).order_by('{}num_assets'.format(col_type[order_type]))
    #    else:
    #        col_relatons = {'0': 'name', '1': 'program_name', '3': 'state', '4': 'offers_bounties', '5': 'max_ammount'}
    #        projects = projects.order_by('{}{}'.format(col_type[order_type], col_relatons[order_col]))

    paginator = Paginator(projects, length)
    try:
        object_list = paginator.page(draw).object_list
    except PageNotAnInteger:
        object_list = paginator.page(draw).object_list
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages).object_list

    """data = [
        {
            'name': {'name': projects.name, 'id': projects.pk},
            'status': projects.status,
            'client': projects.client.name,
            'risk': 'Informative',
            'assets': projects.asset_set.count(),
            'issues': 0,
        } for projects in object_list
    ]"""
    data = []
    for projects in object_list:
        #TODO: serach issues and risk adn changestatus
        
        data.append({
            'name': {'name': projects.name, 'id': projects.pk},
            'status': projects.get_status_display(),
            'client': projects.client.name,
            'risk': 'Informative',
            'assets': projects.asset_set.count(),
            'issues': 0,
        })
    return JsonResponse({'draw': draw, 'recordsTotal': records_total, 'recordsFiltered': records_filtered, 'data': data})

def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()

    return redirect('projects')

def project_del(request, project):
    project = Project.objects.get(id=project)
    if project:
        project.delete()
    return redirect('/projects/')

def project_info(request, project):
    instance = get_object_or_404(Project, pk=project)
    if not request.user.groups.filter(name=instance.client).exists():
        return redirect('projects')
    
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

    context = {
        'project': instance,
        'form': form,
        'risks': None,
    }
    return render(request, 'app/project_info.html', context)

def project_asset(request, project):
    instance = get_object_or_404(Project, id=project)
    return render(request, "app/project_asset.html", {'project': instance, 'form': AssetForm})

def project_vuln(request, project):
    assets = Asset.objects.filter(project=project)
    vulns = []
    for asset in assets:
        for vuln in asset.vulnerabilities.all():
            vulns.append(vuln)

    context = {
        'project': Project.objects.get(id=project),
        'assets': assets,
        'vulnerabilities': vulns,
    }
    return render(request, "app/project_vuln.html", context)

# ASSETS
def assets_data(request, project):
    datatables = request.GET
    draw = int(datatables.get('draw'))
    start = int(datatables.get('start'))
    length = int(datatables.get('length'))
    search = datatables.get('search[value]')
    order_col = datatables.get('order[0][column]')
    order_type = datatables.get('order[0][dir]', 'asc')

    instance = get_object_or_404(Project, pk=project)
    if not request.user.groups.filter(name=instance.client).exists():
        return JsonResponse({'draw': draw, 'recordsTotal': 0, 'recordsFiltered': 0, 'data': []})

    assets = instance.asset_set.all()
    records_total = assets.count()
    records_filtered = assets.count()

    if search:
        assets = assets.filter(
                Q(name__icontains=search)|
                Q(type__icontains=search)
            )
        records_total = assets.count()
        records_filtered = records_total

    if order_col:
        col_type = {'asc': '', 'desc': '-'}
        if order_col == '3':
            assets = assets.annotate(num_vulns=Count('vulnerabilities')).order_by('{}num_vulns'.format(col_type[order_type]))
        else:
            col_relatons = {'0': 'name', '1': 'type', '3': 'risk', '4': 'vulnerabilities'}
            assets = assets.order_by('{}{}'.format(col_type[order_type], col_relatons[order_col]))

    paginator = Paginator(assets, length)
    try:
        object_list = paginator.page(draw).object_list
    except PageNotAnInteger:
        object_list = paginator.page(draw).object_list
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages).object_list

    """data = [
        {
            'name': {'name': projects.name, 'id': projects.pk},
            'status': projects.status,
            'client': projects.client.name,
            'risk': 'Informative',
            'assets': projects.asset_set.count(),
            'issues': 0,
        } for projects in object_list
    ]"""
    data = []
    for asset in object_list:        
        data.append({
            'name': {'name': asset.name, 'id': asset.pk},
            'type': asset.get_type_display(),
            'risk': 'Informative',
            'vulnerabilities': asset.vulnerabilities.count()
        })
    return JsonResponse({'draw': draw, 'recordsTotal': records_total, 'recordsFiltered': records_filtered, 'data': data})

def asset_add(request, project):
    if request.method == 'POST':
        instance = get_object_or_404(Project, id=project)
        form = AssetForm(request.POST)
        if form.is_valid():          
            asset = Asset(
                name=form.cleaned_data['name'], 
                type=form.cleaned_data['type'],
                notes=form.cleaned_data['notes'],
                project=instance
            )
            asset.save()
    
    return redirect('project_asset', project=project)

def asset_mod(request, project, asset):
    instance = get_object_or_404(Asset, pk=asset)
    form = AssetForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_asset', project=project)
    
    return render(request, "app/asset_mod.html", {'asset': instance, 'project': project, 'form': form})

def asset_del(request, project, asset):
    instance = get_object_or_404(Asset, pk=asset)
    instance.delete()
    return redirect('project_asset', project=project)

# VULNERABILITIES
def vuln_add(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_mod(request, project):
    return redirect('/project/{0}/'.format(project))

def vuln_del(request, project):
    return redirect('/project/{0}/'.format(project))

# API
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer