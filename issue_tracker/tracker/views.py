from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import (
    View,
    TemplateView,
    FormView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode

from .models import Issue, Project
from .forms import IssueForm, SearchForm, ProjectForm


# Create your views here.
class IndexView(ListView):
    template_name = 'issue/index.html'
    model = Issue
    context_object_name = 'issues'
    ordering = ('updated_at')
    paginate_by=10
    paginate_orphans=2

    def get(self,request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_data) |
                Q(description__icontains=self.search_data))
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context

class IndexProjectView(ListView):
    template_name = 'project/index.html'
    model = Project
    context_object_name = 'projects'

    def get(self,request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexProjectView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data) |
                Q(description__icontains=self.search_data))
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context

class Issue_view(TemplateView):
    template_name = 'issue/view.html'

    def get_context_data(self, **kwargs):
        kwargs['issue']=get_object_or_404(Issue, pk=kwargs.get('pk'))
        return super().get_context_data(**kwargs)

class ProjectView(DetailView):
    template_name = 'project/view.html'
    queryset = Project.objects.all()
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    template_name = 'project/create.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project-view', kwargs={'pk': self.object.pk})

class ProjectUpdateView(UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'project/update.html'
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('project-view', kwargs={'pk':self.object.pk})

class ProjectDeleteView(DeleteView):
    template_name = 'project/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('project-list')

class IssueCreateView(FormView):
    form_class = IssueForm
    template_name = 'issue/create.html'

    def form_valid(self, form):
        types=form.cleaned_data.pop('type')
        self.issue = Issue.objects.create(
            summary=form.cleaned_data.get('summary'),
            description=form.cleaned_data.get('description'),
            status=form.cleaned_data.get('status'),
            project=get_object_or_404(Project, id=self.kwargs.get('pk'))
        )
        self.issue.type.set(types)
        self.issue.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue-view', kwargs={'pk':self.issue.pk})


class IssueUpdateView(UpdateView):
    form_class = IssueForm
    template_name = 'issue/update.html'
    model = Issue
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('issue-view', kwargs={'pk': self.object.pk})

class Issue_delete(DeleteView):
    model = Issue
    template_name = 'issue/delete.html'
    context_object_name = 'issue'

    def get_success_url(self):
        print(self.object.project.pk)
        return reverse('project-view', kwargs={'pk':self.object.project.pk})

