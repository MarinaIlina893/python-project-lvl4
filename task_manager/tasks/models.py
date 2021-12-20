from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    description = models.CharField(max_length=100, null=True, verbose_name=_('Описание'))
    executor = models.ForeignKey(User, related_name='executor',
                                 on_delete=models.CASCADE, null=True,
                                 verbose_name=_('Исполнитель'))
    author = models.ForeignKey(User, related_name='author',
                               on_delete=models.CASCADE, editable=False,
                               verbose_name=_('Автор'))
    status = models.ForeignKey(Status, on_delete=models.CASCADE,
                               verbose_name=_('Статус'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Дата создания'))
    labels = models.ManyToManyField('labels.Label',
                                    related_name='labels', blank=True,
                                    verbose_name=_('Метки'))
    objects = models.Manager()
