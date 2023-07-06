from django.contrib.auth.decorators import login_required



def login_required_decorator(f):
    return login_required(f)