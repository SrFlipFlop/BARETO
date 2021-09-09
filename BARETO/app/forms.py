from django import forms
from datetime import date, timedelta
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