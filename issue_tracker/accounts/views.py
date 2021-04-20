from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator

from django.views.generic import DetailView, ListView
from accounts.models import Profile
from accounts.forms import UserRegisterForm


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

class UserDetailView(LoginRequiredMixin, DetailView):

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
        kwargs['is_paginated']=page.has_other_pages()
        print('UserDetailView')
        return super().get_context_data(**kwargs)

class UserListView(PermissionRequiredMixin,ListView):
    permission_required = 'tracker.can_view_profiles'
    template_name = 'users.html'
    model = get_user_model()
    context_object_name = 'users'
