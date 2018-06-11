from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from accounts.api.tokens import account_activation_token

# Create your views here.
def register_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('verified')
    else:
        return HttpResponse('failed')