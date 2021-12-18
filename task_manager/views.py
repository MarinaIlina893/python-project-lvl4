from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth import views as auth_views
from task_manager.utils import MessageMixin
from django import forms
from django.contrib.auth.models import User


def index(request):
    return render(request, 'task_manager/base.html')


"""class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields['username'].widget.attrs['placeholder'] = field.label"""


class UserLoginView(MessageMixin, auth_views.LoginView):
    success_message = _("You are logged in")
    error_message = _("Something went wrong")
