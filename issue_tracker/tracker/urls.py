from django.urls import path

from .views import (
    IndexView,
    Issue_view,
    Issue_create,
    Issue_update,
)

urlpatterns=[
    path('',IndexView.as_view() , name = 'issue-list'),
    path('issue/<int:pk>', Issue_view.as_view(), name='issue-view'),
    path('issue/new',Issue_create.as_view(), name = 'issue-create' ),
    path('issue/<int:pk>/edit',Issue_update.as_view(), name='issue-update' ),

]