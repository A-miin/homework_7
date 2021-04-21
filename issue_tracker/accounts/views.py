from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator

from django.views.generic import DetailView, ListView, UpdateView
from accounts.models import Profile
from accounts.forms import UserRegisterForm, UserChangeForm, ProfileChangeForm, PasswordUpdateForm


def register_view(request, *args, **kwargs):
    if request.method=='POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('tracker:project-list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/create.html', context={'form':form})

class UserDetailView(DetailView):

    model = get_user_model()
    template_name = 'user_view.html'
    context_object_name = 'user_object'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        projects = self.object.projects.filter(is_deleted=False)
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        # can update?
        kwargs['can_update'] = self.request.user==self.get_object()

        kwargs['is_paginated']=page.has_other_pages()
        return super().get_context_data(**kwargs)

class UserListView(PermissionRequiredMixin,ListView):
    permission_required = 'tracker.can_view_profiles'
    template_name = 'users.html'
    model = get_user_model()
    context_object_name = 'users'

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_update.html'
    context_object_name = 'user_object'
    profile_form_class = ProfileChangeForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form']=kwargs.get('profile_form')
        if context['profile_form'] is None:
            context['profile_form']=self.get_profile_form()
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        response = super().form_valid(user_form)
        profile_form.save()
        return response

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(self, form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance':self.object.profile }
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return self.profile_form_class(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk':self.object.pk})

class UserPasswordUpdateView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    template_name = 'user_password_update.html'
    form_class = PasswordUpdateForm
    context_object_name = 'user_object'

    def get_success_url(self):
        return reverse('accounts:login')
    def get_object(self, queryset=None):
        return self.request.user