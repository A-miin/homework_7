from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View, TemplateView, FormView
from django.urls import reverse

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


class IssueCreateView(FormView):
    form_class = IssueForm
    template_name = 'issue_create.html'

    def form_valid(self, form):
        types=form.cleaned_data.pop('type')
        self.issue = Issue.objects.create(
            summary=form.cleaned_data.get('summary'),
            description=form.cleaned_data.get('description'),
            status=form.cleaned_data.get('status')
        )
        self.issue.type.set(types)
        self.issue.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-view', kwargs={'pk':self.issue.pk})


class IssueUpdateView(FormView):
    form_class = IssueForm
    template_name = 'issue_update.html'

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance']=self.issue
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['issue'] = self.issue
        return context

    def form_valid(self, form):
        types = form.cleaned_data.pop('type')
        form.save()
        self.issue.type.set(types)
        return super().form_valid(form)

    def get_object(self):
        issue = get_object_or_404(Issue, id=self.kwargs.get('pk'))
        return issue

    def get_success_url(self):
        return reverse('issue-view', kwargs={'pk':self.kwargs.get('pk')})

class Issue_delete(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs['pk'])
        return render(request, 'issue_delete.html', context={'issue':issue})
    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs['pk'])
        if request.POST.get('action')=='Да':
            issue.delete()
            return redirect('issue-list')
        else:
            return redirect('issue-view', issue.id)

