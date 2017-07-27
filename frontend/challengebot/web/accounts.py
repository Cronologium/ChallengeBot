import re
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

def auth_ajax(request):
    if request.user.is_authenticated:
        logout(request)
    if 'username' in request.POST and 'password' in request.POST:
        if request.POST['username'] == '':
            return JsonResponse({'msg': 'Empty username.'})
        if request.POST['password'] == '':
            return JsonResponse({'msg': 'Empty password.'})
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': 'Invalid username or password'})
    return JsonResponse({'msg': 'Missing username or password'})


def check_empty_fields(request):
    if 'username' not in request.POST:
        return {'reg-user-err': 'Please enter a username'}
    if 'email' not in request.POST:
        return {'reg-email-error': 'Please enter an e-mail address'}
    if 'password' not in request.POST:
        return {'reg-pass-error': 'Please enter a password'}
    if 'confirm-password' not in request.POST:
        return {'reg-confirm-error': 'Please confirm password'}
    return None


def validate_username(request):
    if request.POST['username'] == '':
        return {'reg-user-error': 'Please enter a username'}
    username = request.POST['username']
    if len(username) < 8:
        return {'reg-user-error': 'Username must contain at least 8 characters.'}
    if len(username) > 20:
        return {'reg-user-error': 'Username must contain at most 20 characters.'}
    if not re.match(r'^[A-Za-z].*', username):
        return {'reg-user-error': 'Username does not start with a letter'}
    if User.objects.filter(username=username).exists():
        return {'reg-user-error': 'Username is taken.'}
    if not re.match(r'^\w+$', username):
        return {'reg-user-error': 'Username can only contain letters, numbers and the underscore'}
    return None


def validate_email(request):
    if request.POST['email'] == '':
        return {'reg-email-error': 'Please enter an e-mail address.'}
    email = request.POST['email']
    if len(email) > 254:
        return {'reg-email-error': 'E-mail address is too long'}
    if User.objects.filter(email=email).exists():
        return {'reg-email-error': 'E-mail address already in use'}
    if re.search(r"[^@]+@[^@]+\.[a-zA-Z]+", email) is None:
        return {'reg-email-error': 'E-mail address looks invalid'}
    return None


def validate_password(request):
    if request.POST['password'] == '':
        return {'reg-pass-error': 'Please enter a password'}
    password = request.POST['password']
    if len(password) < 8:
        return {'reg-pass-error': 'Password too short.'}
    if len(password) > 35:
        return {'reg-pass-error': 'Password too long. How will you remember that?'}
    if not re.match(r'[A-Za-z0-9@#$%^&+=()!_*{}:;/".,?~`<>| \-\'\[\]\\]{8,35}', password):
        return {'reg-pass-error': 'Password contains invalid characters.'}
    if not re.search(r'[A-Za-z]+', password):
        return {'reg-pass-error': 'Password does not contain letters'}
    if not re.search(r'[0-9]+', password):
        return {'reg-pass-error': 'Password does not contain digits'}
    if not re.search(r'[^A-Za-z0-9]+', password):
        return {'reg-pass-error': 'Password does not contain symbols'}
    if password == request.POST['email']:
        return {'reg-pass-error': 'Password cannot match email address'}
    if password == request.POST['username']:
        return {'reg-pass-error': 'Password cannot match username'}
    return None


def validate_confirm_password(request):
    if request.POST['confirm-password'] == '':
        return {'reg-confirm-error': 'Please confirm password'}
    confirm_password = request.POST['confirm-password']
    if len(confirm_password) != len(request.POST['password']) or confirm_password != request.POST['password']:
        return {'reg-confirm-error': 'Passwords do not match!'}
    return None


def reg_ajax(request):
    err = False
    errors = {}
    empty_check = check_empty_fields(request)
    if empty_check is not None:
        return empty_check

    username_check = validate_username(request)
    if username_check is not None:
        err = True
        for key in username_check:
            errors[key] = username_check[key]

    email_check = validate_email(request)
    if email_check is not None:
        err = True
        for key in email_check:
            errors[key] = email_check[key]

    password_check = validate_password(request)
    if password_check is not None:
        err = True
        for key in password_check:
            errors[key] = password_check[key]

    confirm_check = validate_confirm_password(request)
    if confirm_check is not None:
        err = True
        for key in confirm_check:
            errors[key] = confirm_check[key]

    if not err:
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        user.save()
        return JsonResponse({'': ''})
    else:
        return JsonResponse(errors)