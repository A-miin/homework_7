from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View, TemplateView, FormView, ListView
from django.urls import reverse
from django.db.models import Q
from django.utils.http import urlencode

from .models import Issue, Project
from .forms import IssueForm, SearchForm


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

class Project_view(TemplateView):
    template_name = 'project/'

class IssueCreateView(FormView):
    form_class = IssueForm
    template_name = 'issue/create.html'

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
    template_name = 'issue/update.html'

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
        return render(request, 'issue/delete.html', context={'issue':issue})
    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs['pk'])
        if request.POST.get('action')=='Да':
            issue.delete()
            return redirect('issue-list')
        else:
            return redirect('issue-view', issue.id)

