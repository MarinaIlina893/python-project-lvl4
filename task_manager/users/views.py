from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from task_manager.utils import MessageMixin


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserCreate(MessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    success_url = '/login/'
    template_name = 'auth/user_form.html'
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdate(UpdateView):
    model = User
    success_url = '/users/'
    template_name = 'auth/user_update.html'
    form_class = UpdateUserForm


class UserDelete(DeleteView):
    model = User
    success_url = '/login'


class UserListView(ListView):
    model = User
    paginate_by = 30
