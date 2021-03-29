from django.urls import path

from .views import (
    IndexView,
    Issue_view,
    Issue_delete,
    IssueCreateView,
    IssueUpdateView,
    IndexProjectView,
    ProjectView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)

urlpatterns=[
    path('',IndexProjectView.as_view() , name = 'project-list'),
    path('project/<int:pk>',ProjectView.as_view() , name = 'project-view'),
    path('project/new',ProjectCreateView.as_view(), name='project-create' ),
    path('project/<int:pk>/edit',ProjectUpdateView.as_view(), name='project-update' ),
    path('project/<int:pk>/delete',ProjectDeleteView.as_view(), name='project-delete'),
    path('issues',IndexView.as_view() , name = 'issue-list'),
    path('issue/<int:pk>', Issue_view.as_view(), name='issue-view'),
    path('issue/<int:pk>/new',IssueCreateView.as_view(), name = 'issue-create' ),
    path('issue/<int:pk>/edit',IssueUpdateView.as_view(), name='issue-update' ),
    path('issue/<int:pk>/delete', Issue_delete.as_view(), name ='issue-delete'),

]