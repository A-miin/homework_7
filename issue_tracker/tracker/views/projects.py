# from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode

from tracker.models import Issue, Project
from tracker.forms import IssueForm, SearchForm, ProjectForm


# Create your views here.
class IndexProjectView(ListView):
    template_name = 'project/index.html'
    model = Project
    context_object_name = 'projects'

    def get(self,request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexProjectView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = Project.objects.filter(is_deleted=False)

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data) |
                Q(description__icontains=self.search_data) |
                Q(is_deleted=False))
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


class ProjectView(DetailView):
    template_name = 'project/view.html'
    queryset = Project.objects.filter(is_deleted=False)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset

class ProjectDeleteView(DeleteView):
    template_name = 'project/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('project-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset
