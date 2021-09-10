from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from datetime import date, timedelta

from django.forms import widgets
from tinymce.widgets import TinyMCE

from app.models import *

class ProjectForm(forms.ModelForm):
    name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.ChoiceField(choices=PROJECT_STATUS, widget=forms.Select(attrs={'class':'custom-select'}))
    start = forms.DateTimeField(
        initial=date.today, 
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#startProject'
        })
    )    
    finished = forms.DateTimeField(
        initial=date.today() + timedelta(days=30), 
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#finishProject'
        })
    )
    notes = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Project
        fields = '__all__'

class UserClientCreateForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class':'custom-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'groups']
    
    def __init__(self, *args, **kwargs):
        super(UserClientCreateForm, self).__init__(*args, **kwargs)
        for element in ['username', 'password1', 'password2']:
            self.fields[element].widget.attrs.update({'class':'form-control'})

class UserClientUpdateForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class':'custom-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'groups']
    
    def __init__(self, *args, **kwargs):
        super(UserClientUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
