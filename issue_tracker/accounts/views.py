from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate


# Create your views here.

def login(request, *args, **kwargs):
    context={}
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('article-list')
        else:
            context['has_error']=True

    return render(request,'login.html', context=context)