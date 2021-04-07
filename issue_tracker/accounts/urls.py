from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import login_view, logout_view
#

urlpatterns=[
    # path('login', LoginView.as_view(), name='login' ),
    # path('logout', LogoutView.as_view(), name='logout' ),
    path('logout', logout_view, name='logout' ),
    path('login', login_view , name='login' ),

]