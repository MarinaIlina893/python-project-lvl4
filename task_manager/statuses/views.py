from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django import forms
from .models import Status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from task_manager.utils import MessageMixin


# Create your views here.
class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    name = forms.CharField(label=_("Имя"))


class StatusCreate(LoginRequiredMixin, MessageMixin, CreateView):
    model = Status
    form_class = CreateStatusForm
    success_url = '/statuses/'
    template_name = 'status_create_form.html'
    success_message = "Статус успешно создан"


class StatusListView(ListView):
    model = Status
    paginate_by = 30
    template_name = 'status_list.html'


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    name = forms.CharField(label=_("Имя"))


class StatusUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    model = Status
    form_class = UpdateStatusForm
    success_url = '/statuses/'
    template_name = 'status_update_form.html'
    success_message = "Статус успешно изменён"


class DeleteStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class StatusDelete(LoginRequiredMixin, FormMixin, DeleteView):
    model = Status
    form_class = DeleteStatusForm
    success_url = '/statuses/'
    template_name = 'status_delete_form.html'
    error_message = _("Нельзя удалить статус. Он используется в задачах")
    success_message = "Статус успешно удалён"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.task_set.all():
            self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(self.get_context_data(**kwargs)['form'])
