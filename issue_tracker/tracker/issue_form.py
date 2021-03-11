from django import forms
from .models import Issue, Type, Status

class IssueForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label='Тип')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус')
    class Meta:
        model=Issue
        fields=('summary', 'description')