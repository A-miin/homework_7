from django.urls import path

from tracker.views import (
    IndexView,
    IssueView,
    IssueDeleteView,
    IssueCreateView,
    IssueUpdateView,
    IndexProjectView,
    ProjectView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)

app_name='tracker'
urlpatterns=[
    path('',IndexProjectView.as_view() , name = 'project-list'),
    path('project/<int:pk>',ProjectView.as_view() , name = 'project-view'),
    path('project/new',ProjectCreateView.as_view(), name='project-create' ),
    path('project/<int:pk>/edit',ProjectUpdateView.as_view(), name='project-update' ),
    path('project/<int:pk>/delete',ProjectDeleteView.as_view(), name='project-delete'),
    path('issues',IndexView.as_view() , name = 'issue-list'),
    path('issue/<int:pk>', IssueView.as_view(), name='issue-view'),
    path('issue/<int:pk>/new',IssueCreateView.as_view(), name = 'issue-create' ),
    path('issue/<int:pk>/edit',IssueUpdateView.as_view(), name='issue-update' ),
    path('issue/<int:pk>/delete', IssueDeleteView.as_view(), name ='issue-delete'),

]