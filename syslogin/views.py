from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth

def login(request):
    args={}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('sport:competition')
        else:
            args['login_error'] = "Неверный логин или пароль"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')
