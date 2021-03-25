from django import forms
from django.core.exceptions import ValidationError

from .models import Issue, Type

class IssueForm(forms.ModelForm):
    type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Type.objects.all(), label='Тип')
    class Meta:
        model=Issue
        fields=('summary', 'description', 'type', 'status')

class SearchForm(forms.Form):
    search_value = forms.CharField(max_length=100, required=False, label='Найти')
