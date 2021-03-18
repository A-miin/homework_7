from django.urls import path

from .views import (
    IndexView,
    Issue_view,
    Issue_delete,
    IssueCreateView,
    IssueUpdateView,
)

urlpatterns=[
    path('',IndexView.as_view() , name = 'issue-list'),
    path('issue/<int:pk>', Issue_view.as_view(), name='issue-view'),
    path('issue/new',IssueCreateView.as_view(), name = 'issue-create' ),
    path('issue/<int:pk>/edit',IssueUpdateView.as_view(), name='issue-update' ),
    path('issue/<int:pk>/delete', Issue_delete.as_view(), name ='issue-delete'),

]