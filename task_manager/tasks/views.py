from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from .models import Task
from task_manager.statuses.models import Status
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
from task_manager.utils import MessageMixin
from task_manager.users.models import User
from django.db.models import QuerySet


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'labels': _('Метки'),
        }

class TaskCreate(LoginRequiredMixin, MessageMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    success_url = '/tasks/'
    template_name = 'task_create_form.html'
    success_message = "Задача успешно создана"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['executors'] = User.objects.all()
        return context

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




"""class CustomQuerySet(QuerySet):
    def annotate_with_custom_field(self):
        return self.annotate(
            custom_field=('user__first_name'),
                default=None,
            )"""
class TaskFilter(LoginRequiredMixin, django_filters.FilterSet):

    """class MyModelChoiceFilter(django_filters.ModelChoiceFilter):

        def label_from_instance(self, obj):
            return "{first_name} {last_name}".format(
                first_name=obj.first_name, last_name=obj.last_name)"""

    """class MyModelChoiceFilter(django_filters.ModelChoiceFilter):
        def get_filter_predicate(self, v):
            return {'first_name': v.annotated_field}

        def filter(self, qs, value):
            if value:
                qs = qs.annotate_with_custom_field()
                qs = super().filter(qs, value)
            return qs"""





    """class User:
        objects = CustomQuerySet.as_manager()"""

    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['executor'].label_from_instance = lambda obj: "%s %s" % (obj.last_name, obj.first_name)"""

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
                                          widget=forms.CheckboxInput,
                                          method='my_custom_filter')


    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'author']

    def my_custom_filter(self, queryset, name, value):
        return queryset


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    paginate_by = 30
    template_name = 'task_list.html'
    filterset_class = TaskFilter

    def get_queryset(self):
        if self.request.GET.get('author') == 'on':
            qs = self.model.objects.filter(author=self.request.user)
            task_filtered_list = TaskFilter(self.request.GET, queryset=qs)
            return task_filtered_list.qs
        qs = self.model.objects.all()
        task_filtered_list = TaskFilter(self.request.GET, queryset=qs)
        return task_filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['executors'] = User.objects.values('id', 'first_name', 'last_name')
        context['current_executor'] = int(str(self.request.GET.get('executor')))

        return context

