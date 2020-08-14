# This file consist of all the user created decorators
# It is meant for user role based permissions and authentication

from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    # redirects user to index page if user is logged in
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    # restricts users that are allowed on each page to specified user groups
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('index')
        return wrapper_func
    return decorator

