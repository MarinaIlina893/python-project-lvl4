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

    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def clean_password2(self):
        new_password1 = self.cleaned_data.get('password1')
        new_password2 = self.cleaned_data.get('password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(new_password2)
        return new_password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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


class UserUpdate(MessageMixin, UpdateView):
    model = User
    success_url = '/users/'
    template_name = 'auth/user_update.html'
    form_class = UpdateUserForm
    success_message = "Пользователь успешно изменён"


class UserDelete(DeleteView):
    model = User
    success_url = '/login'


class UserListView(ListView):
    model = User
    paginate_by = 30
