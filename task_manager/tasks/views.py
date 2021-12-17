from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from django.urls import reverse
from django.views.generic import DetailView
import django_filters
from django_filters.views import FilterView


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    success_url = '/tasks/'
    template_name = 'task_create_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super().form_valid(form)


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    success_url = '/tasks/'
    template_name = 'task_update_form.html'


class DeleteTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']


class TaskDelete(LoginRequiredMixin, FormMixin, DeleteView):
    model = Task
    success_url = '/tasks/'
    template_name = 'task_delete_form.html'
    success_message = _("You are logged in")
    error_message = _("Something went wrong")
    form_class = DeleteTaskForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.author == request.user:
            messages.error(self.request, self.error_message)
            return HttpResponseRedirect(reverse('tasks'))
        return super().get(self, request, args, *kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(self.get_context_data(**kwargs)['form'])


class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail_form.html'
    form_class = TaskDetailForm
    context_object_name = 'task'


class TaskFilter(django_filters.FilterSet):

    status = django_filters.ModelChoiceFilter(field_name='status',
                                              label='Статус',
                                              queryset=Status.objects.all())

    executor = django_filters.ModelChoiceFilter(field_name='executor',
                                                label='Исполнитель',
                                                queryset=User.objects.all())

    labels = django_filters.ModelMultipleChoiceFilter(
        field_name='labels',
        label='Метки',
        queryset=Label.objects.all())

    author = django_filters.BooleanFilter(field_name='author',
                                          label='Только свои задачи',
                                          method='my_custom_filter',
                                          widget=forms.CheckboxInput)

    class Meta:
        model = Task
        fields = ['status']

    def my_custom_filter(self, queryset, name, value):
        if value:
            user = getattr(self.request, 'user', None)
            return Task.objects.filter(author=user)
        return queryset


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    paginate_by = 30
    template_name = 'task_list.html'
    filterset_class = TaskFilter

    def get_queryset(self):
        qs = self.model.objects.all()
        task_filtered_list = TaskFilter(self.request.GET, queryset=qs)
        return task_filtered_list.qs
