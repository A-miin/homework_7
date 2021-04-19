from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import register_view, UserDetailView, UserListView
#

app_name='accounts'
urlpatterns=[
    path('login', LoginView.as_view(), name='login' ),
    path('logout', LogoutView.as_view(), name='logout' ),
    path('register', register_view, name='register'),
    path('<int:pk>/profile', UserDetailView.as_view(), name='profile'),
    path('users', UserListView.as_view(), name='users' )
    # path('logout', logout_view, name='logout' ),
    # path('login', login_view , name='login' ),

]