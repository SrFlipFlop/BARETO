from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from app.models import *
from app.serializers import *
from app.forms import *

@login_required
def index(request):
    return render(request, "app/dashboard.html", {})

def max_risk(vulns):
    risks = ('Informative', 'Low', 'Medium', 'High', 'Critical')
    index = max([risks.index(v.risk) for k, v in vulns.iteritems()])
    return risks[index]

# CLIENTS
@login_required
def clients(request):
    context = {'users': [], 'clients': [], 'form': UserClientCreateForm}
    for user in User.objects.all():
        context['users'].append({
            'id': user.pk,
            'name': user.username,
            'clients': ', '.join([g.name for g in user.groups.all()]),
        })
    
    for group in Group.objects.all():
        context['clients'].append({
            'id': group.pk,
            'name': group.name,
            'projects': Project.objects.filter(client__name=group.name).count(),
            'users': User.objects.filter(groups__name=group.name).count(),
        })

    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']

    return render(request, "app/clients.html", context)

@login_required
def clients_add_group(request):
    if request.method == 'POST' and request.user.is_staff:
        new_group, created = Group.objects.get_or_create(name=request.POST.get('clientName', 'Default'))
    return redirect('clients')

@login_required
def clients_mod_group(request, group):
    if request.user.is_staff:
        instance = get_object_or_404(Group, pk=group)
        if request.method == 'GET':
            return render(request, "app/client_mod.html", {'current': instance})
        else:
            new_name = request.POST.get('clientName')
            if not Group.objects.filter(name=new_name):
                instance.name = new_name
                instance.save()

    return redirect('clients')

@login_required
def clients_del_group(request, group):
    if request.user.is_staff:
        group = get_object_or_404(Group, pk=group)
        group.delete()
    return redirect('clients')

@login_required
def clients_add_user(request):
    if request.method == 'POST' and request.user.is_staff:
        form = UserClientCreateForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password1'])
            for group in form.cleaned_data['groups']:
                new_user.groups.add(group)
            new_user.save()
        else:
            request.session['error'] = form.errors

    return redirect('clients')

@login_required
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

@login_required
def clients_del_user(request, user):
    if request.user.is_staff:
        user = get_object_or_404(User, pk=user)
        user.delete()
    return redirect('clients')

# PROJECTS
@login_required
def projects(request):
    context = {'form': ProjectForm(user=request.user)}
    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']
    
    return render(request, "app/projects.html", context)

@login_required
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

@login_required
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            request.session['error'] = form.errors

    return redirect('projects')

@login_required
def project_del(request, project):
    project = Project.objects.get(id=project)
    if project:
        project.delete()
    return redirect('/projects/')

@login_required
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

@login_required
def project_asset(request, project):
    instance = get_object_or_404(Project, id=project)
    return render(request, "app/project_asset.html", {'project': instance, 'form': AssetForm})

@login_required
def project_vuln(request, project):
    instance = get_object_or_404(Project, id=project)
    context = {
        'project': instance,
        'assets': instance.asset_set.all(),
        'templates': Template.objects.all(),
        'form': VulnerabilityForm(project=instance),
    }
    return render(request, "app/project_vuln.html", context)

# ASSETS
@login_required
def assets(request):
    projects = Project.objects.filter(client__in=request.user.groups.all())
    context = {'assets':[]}
    for asset in Asset.objects.filter(project__in=projects):
        context['assets'].append({
            'name': asset.name,
            'type': asset.get_type_display(),
            'risk': asset.vulnerabilities.order_by('-risk').first().get_risk_display(),
            'project': asset.project,
            'vulnerabilities': asset.vulnerabilities.count(),
        })

    return render(request, "app/assets.html", context)

@login_required
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

@login_required
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

@login_required
def asset_mod(request, project, asset):
    instance = get_object_or_404(Asset, pk=asset)
    form = AssetForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('project_asset', project=project)
    
    return render(request, "app/asset_mod.html", {'asset': instance, 'project': project, 'form': form})

@login_required
def asset_del(request, project, asset):
    instance = get_object_or_404(Asset, pk=asset)
    instance.delete()
    return redirect('project_asset', project=project)

# VULNERABILITIES
@login_required
def vulns(request):
    if 'draw' not in request.GET:
        return render(request, "app/vulns.html", {'vulns': vulns})
    
    datatables = request.GET
    draw = int(datatables.get('draw'))
    start = int(datatables.get('start'))
    length = int(datatables.get('length'))
    search = datatables.get('search[value]')
    order_col = datatables.get('order[0][column]')
    order_type = datatables.get('order[0][dir]', 'asc')

    projects = Project.objects.filter(client__in=request.user.groups.all())
    #instance = get_object_or_404(Project, pk=project)
    #if not request.user.groups.filter(name=instance.client).exists():
    #    return JsonResponse({'draw': draw, 'recordsTotal': 0, 'recordsFiltered': 0, 'data': []})

    query = Q()
    for project in projects:
        for asset in project.asset_set.all():
            query = query | Q(asset__pk=asset.pk)

    #TODO: Group vulns by assets --> {'Vuln1': ['asset1','asset2']}
    vulnerabilities = Vulnerability.objects.filter(query)
    records_total = vulnerabilities.count()
    records_filtered = vulnerabilities.count()

    if search:
        vulnerabilities = vulnerabilities.filter(
                Q(name__icontains=search)|
                Q(type__icontains=search)
            )
        records_total = vulnerabilities.count()
        records_filtered = records_total

    if order_col:
        col_type = {'asc': '', 'desc': '-'}
        #if order_col == '3':
        #    assets = vulnerabilities.annotate(num_vulns=Count('vulnerabilities')).order_by('{}num_vulns'.format(col_type[order_type]))
        #else:
        #    col_relatons = {'0': 'name', '1': 'type', '3': 'risk', '4': 'vulnerabilities'}
        #    assets = vulnerabilities.order_by('{}{}'.format(col_type[order_type], col_relatons[order_col]))

    paginator = Paginator(vulnerabilities, length)
    try:
        object_list = paginator.page(draw).object_list
    except PageNotAnInteger:
        object_list = paginator.page(draw).object_list
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages).object_list

    data = []
    for vulnerability in object_list:
        data.append({
            'name': {'name': vulnerability.name, 'id': vulnerability.pk, 'project': vulnerability.asset_set.first().project.pk},
            'risk': vulnerability.get_risk_display(),
            'category': vulnerability.get_type_display(),
            'status': vulnerability.get_status_display(),
            'assets': '<br>'.join([asset.name for asset in vulnerability.asset_set.all()]),
            'project': vulnerability.asset_set.first().project.name,
            'client': vulnerability.asset_set.first().project.client.name,
        })
    return JsonResponse({'draw': draw, 'recordsTotal': records_total, 'recordsFiltered': records_filtered, 'data': data})

@login_required
def vulns_data(request, project):
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

    query = Q()
    for asset in instance.asset_set.all():
        query = query | Q(asset__pk=asset.pk)

    #TODO: Group vulns by assets --> {'Vuln1': ['asset1','asset2']}
    vulnerabilities = Vulnerability.objects.filter(query)
    records_total = vulnerabilities.count()
    records_filtered = vulnerabilities.count()

    if search:
        vulnerabilities = vulnerabilities.filter(
                Q(name__icontains=search)|
                Q(type__icontains=search)
            )
        records_total = vulnerabilities.count()
        records_filtered = records_total

    if order_col:
        col_type = {'asc': '', 'desc': '-'}
        #if order_col == '3':
        #    assets = vulnerabilities.annotate(num_vulns=Count('vulnerabilities')).order_by('{}num_vulns'.format(col_type[order_type]))
        #else:
        #    col_relatons = {'0': 'name', '1': 'type', '3': 'risk', '4': 'vulnerabilities'}
        #    assets = vulnerabilities.order_by('{}{}'.format(col_type[order_type], col_relatons[order_col]))

    paginator = Paginator(vulnerabilities, length)
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
    for vulnerability in object_list:        
        data.append({
            'name': {'name': vulnerability.name, 'id': vulnerability.pk},
            'risk': vulnerability.get_risk_display(),
            'category': vulnerability.get_type_display(),
            'status': vulnerability.get_status_display(),
            'assets': '<br>'.join([asset.name for asset in vulnerability.asset_set.all()]),
        })
    return JsonResponse({'draw': draw, 'recordsTotal': records_total, 'recordsFiltered': records_filtered, 'data': data})

@login_required
def vuln_add(request, project):
    if request.method == 'POST':
        if request.POST.get('addtype') == 'import':
            template = get_object_or_404(Template, pk=request.POST.get('template'))
            new_vuln = Vulnerability(
                name=template.name,
                risk=template.risk,
                cvss=template.cvss,
                status=template.status,
                type=template.type,
                description=template.description,
                impact=template.impact,
                recomendation=template.recomendation
            )
            new_vuln.save()
            for id in request.POST.getlist('assets'):
                asset = get_object_or_404(Asset, pk=id)
                asset.vulnerabilities.add(new_vuln)
                asset.save()
        
        else:
            form = VulnerabilityForm(request.POST)
            if form.is_valid():
                assets = form.cleaned_data['assets']
                del form.cleaned_data['assets']

                new_vuln = Vulnerability(**form.cleaned_data)
                new_vuln.save()
                for asset in assets:   
                    asset.vulnerabilities.add(new_vuln)
                    asset.save()
            else:
                print(f'[!] Form errors - {form.errors}')

    return redirect('project_vuln', project=project)

@login_required
def vuln_mod(request, project, vuln):
    project_instance = get_object_or_404(Project, id=project)
    vuln_instance = get_object_or_404(Vulnerability, id=vuln)
    form = VulnerabilityForm(request.POST or None, instance=vuln_instance, project=project_instance)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('project_vuln', project=project)

    return render(request, "app/vuln_mod.html", {'project': project_instance, 'vulnerability': vuln_instance, 'form': form})

@login_required
def vuln_del(request, project, vuln):
    vuln = get_object_or_404(Vulnerability, pk=vuln)
    vuln.delete()
    return redirect('project_vuln', project=project)

# TEMPLATES
@login_required
def templates(request):
    context = {'form': TemplateForm}
    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']
    
    return render(request, "app/templates.html", context)

@login_required
def templates_data(request):
    datatables = request.GET
    draw = int(datatables.get('draw'))
    start = int(datatables.get('start'))
    length = int(datatables.get('length'))
    search = datatables.get('search[value]')
    order_col = datatables.get('order[0][column]')
    order_type = datatables.get('order[0][dir]', 'asc')

    templates = Template.objects.all()
    records_total = templates.count()
    records_filtered = templates.count()

    if search:
        templates = templates.filter(
                Q(name__icontains=search)|
                Q(status__icontains=search)|
                Q(start__icontains=search)|
                Q(finished__icontains=search)
            )
        records_total = templates.count()
        records_filtered = records_total

    paginator = Paginator(templates, length)
    try:
        object_list = paginator.page(draw).object_list
    except PageNotAnInteger:
        object_list = paginator.page(draw).object_list
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages).object_list

    data = []
    for template in object_list:        
        data.append({
            'name': {'name': template.name, 'id': template.pk},
            'risk': template.get_risk_display(),
            'category': template.get_type_display(),
            'cvss': template.cvss,
        })
    return JsonResponse({'draw': draw, 'recordsTotal': records_total, 'recordsFiltered': records_filtered, 'data': data})

@login_required
def templates_add(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            Template(**form.cleaned_data).save()
        else:
            print(f'[!] Form errors - {form.errors}')
            request.session['error'] = form.errors

    return redirect('templates')

@login_required
def templates_mod(request, template):
    instance = get_object_or_404(Template, pk=template)
    form = TemplateForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
    
    return render(request, 'app/template_mod.html', {'template': instance, 'form': form})

@login_required
def templates_del(request, template):
    instance = get_object_or_404(Template, pk=template)
    instance.delete()
    return redirect('templates')

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