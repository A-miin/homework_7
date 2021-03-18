from django import forms
from .models import Issue, Type, Status

class IssueForm(forms.ModelForm):
    type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Type.objects.all(), label='Тип')
    class Meta:
        model=Issue
        fields=('summary', 'description', 'type', 'status')
