from django import forms
from django.contrib.auth.models import User

from .models import Issue, Type, Project

class IssueForm(forms.ModelForm):
    type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Type.objects.all(), label='Тип')
    class Meta:
        model=Issue
        fields=('summary', 'description', 'type', 'status')

class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=('name', 'description', 'begin_date', 'end_date')

class ProjectUserForm(forms.Form):
    user = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.all(),label="Пользователи")

class ProjectUserForm2(forms.ModelForm):
    user = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.all(),label="Пользователи")

    def __init__(self,request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all().exclude(username=request.user.username)
    class Meta:
        model=Project
        fields=('user',)
