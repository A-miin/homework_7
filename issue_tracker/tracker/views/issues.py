from django.shortcuts import render, get_object_or_404,redirect
# from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
from django.contrib.auth.mixins import LoginRequiredMixin

from tracker.models import Issue, Project
from tracker.forms import IssueForm, SearchForm, ProjectForm


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


class IssueView(DetailView):
    template_name = 'issue/view.html'
    queryset = Issue.objects.all()
    context_object_name = 'issue'

class IssueCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'tracker.add_issue'
    template_name = 'issue/create.html'
    model = Issue
    form_class = IssueForm

    def has_permission(self):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        return super().has_permission() and (self.request.user in project.user.all())

    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        # types=form.cleaned_data.pop('type')

        self.issue = form.save(commit=False)
        self.issue.project = project
        self.issue.save()
        # self.issue.type.set(types)
        form.save_m2m()
        return self.get_success_url()

    def get_success_url(self):
        return redirect('tracker:issue-view', pk = self.issue.id)


class IssueUpdateView(PermissionRequiredMixin,UpdateView):

    def has_permission(self):
        issue= get_object_or_404(Issue, id=self.kwargs.get('pk'))
        return super().has_permission() and (self.request.user in issue.project.user.all())

    permission_required = 'tracker.change_issue'
    form_class = IssueForm
    template_name = 'issue/update.html'
    model = Issue
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse('tracker:issue-view', kwargs={'pk': self.object.pk})

class IssueDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = 'tracker.delete_issue'
    model = Issue
    template_name = 'issue/delete.html'
    context_object_name = 'issue'
    def has_permission(self):
        issue = get_object_or_404(Issue, id=self.kwargs.get('pk'))
        return super().has_permission() and (self.request.user in issue.project.user.all())
    def get_success_url(self):
        print(self.object.project.pk)
        return reverse('tracker:project-view', kwargs={'pk':self.object.project.pk})

