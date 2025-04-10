# login/context_processors.py

from django.contrib.auth.models import User

def user_info(request):
    if request.user.is_authenticated:
        return {'username': request.user.username, 'first_name': request.user.first_name}
    return {'username': None, 'first_name': None}
