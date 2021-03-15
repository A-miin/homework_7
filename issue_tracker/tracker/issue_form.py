from django import forms
from .models import Issue, Type, Status

class IssueForm(forms.ModelForm):
    type = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Type.objects.all(), label='Тип')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус')
    class Meta:
        model=Issue
        fields=('summary', 'description')


  # favorite_colors = forms.MultipleChoiceField(
  #       required=False,
  #       widget=forms.CheckboxSelectMultiple,
  #       choices=FAVORITE_COLORS_CHOICES,
  #   )