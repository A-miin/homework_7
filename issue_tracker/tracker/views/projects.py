from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View, FormView
)
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group

from tracker.models import  Project
from tracker.forms import SearchForm, ProjectForm, ProjectUserForm, ProjectUserForm2


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

class ProjectUserUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'tracker.can_update_members'
    form_class = ProjectUserForm2
    model=Project
    template_name = 'user/update.html'
    context_object_name = 'project'

    def has_permission(self):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))
        print(f'super().has_permission()={super().has_permission()}')
        print(f'(self.request.user in project.user.all())={(self.request.user in project.user.all())}')

        return super().has_permission() and (self.request.user in project.user.all())


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())


    def get_success_url(self):
        return reverse('tracker:project-view', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'tracker.change_project'
    form_class = ProjectForm
    model = Project
    template_name = 'project/update.html'
    context_object_name = 'project'

    def has_permission(self):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'))

        manager_group = Group.objects.get(name="Project Manager")
        print(manager_group)
        return super().has_permission() and manager_group in self.request.user.groups.all()

    def get_success_url(self):
        return reverse('tracker:project-view', kwargs={'pk':self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset

class ProjectView(DetailView):
    template_name = 'project/view.html'
    queryset = Project.objects.filter(is_deleted=False)
    context_object_name = 'project'

class ProjectCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'tracker.add_project'
    template_name = 'project/create.html'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.user.set([self.request.user])
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:project-view', kwargs={'pk': self.object.pk})



class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'tracker.delete_project'
    template_name = 'project/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('tracker:project-list')

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



