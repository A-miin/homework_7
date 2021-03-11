from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View, TemplateView
from .models import Issue
from .issue_form import IssueForm


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        kwargs['issues']=Issue.objects.all()
        return super().get_context_data(**kwargs)

class Issue_view(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        kwargs['issue']=get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().get_context_data(**kwargs)

class Issue_create(View):
    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'issue_create.html', context={'form':form})
    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            issue = Issue.objects.create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
                type=form.cleaned_data.get('type'),
                status=form.cleaned_data.get('status'),
            )
            return redirect('issue-view', pk=issue.pk)
        return render(request, 'issue_create.html',context={'form':form})
