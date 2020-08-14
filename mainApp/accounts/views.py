from django.shortcuts import render, redirect

from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from django.contrib.auth.models import Group

from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    
    context = {
        "form": form
    }
    return render(request,"login.html", context)

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')
        if role == "admin":
            user.is_staff = True
            user.is_superuser = True
        user.set_password(password)        
        user.save()
        
        group = Group.objects.get(name=role)
        user.groups.add(group)
        
        new_user = authenticate(username=user.username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    
    context = {
        "form": form
    }
    return render(request,"signup.html", context)

def logout_view(request):
    logout(request)
    return redirect('/')