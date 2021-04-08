from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tracker:project-list')
        else:
            context['has_error']=True
    return render(request, 'registration/login.html', context=context)

def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('tracker:issue-list')
