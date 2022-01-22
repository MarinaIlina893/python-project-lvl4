from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django import forms
from .models import Label
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from task_manager.utils import MessageMixin


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
    name = forms.CharField(label=_('Имя'))


class LabelCreate(LoginRequiredMixin, MessageMixin, CreateView):
    model = Label
    form_class = CreateLabelForm
    success_url = '/labels/'
    template_name = 'label_create_form.html'
    success_message = "Метка успешно создана"


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    paginate_by = 30
    template_name = 'label_list.html'


class UpdateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
    name = forms.CharField(label=_('Имя'))


class LabelUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    model = Label
    form_class = UpdateLabelForm
    success_url = '/labels/'
    template_name = 'label_update_form.html'
    success_message = "Метка успешно изменена"


class DeleteLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']


class LabelDelete(LoginRequiredMixin, FormMixin, MessageMixin, DeleteView):
    model = Label
    success_url = '/labels/'
    template_name = 'label_delete_form.html'
    form_class = DeleteLabelForm

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        label_tasks = self.object.tasks.all()
        if not label_tasks:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url(),
                                        messages.add_message(
                                            request=self.request,
                                            message="Метка успешно удалена", level=50))
        else:
            return self.form_invalid(self.get_context_data(**kwargs)['form'])
