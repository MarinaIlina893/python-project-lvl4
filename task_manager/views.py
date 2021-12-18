from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth import views as auth_views
from task_manager.utils import MessageMixin
from django import forms


def index(request):
    return render(request, 'task_manager/base.html')


class UserLoginView(MessageMixin, auth_views.LoginView):
    success_message = _("You are logged in")
    error_message = _("Something went wrong")
