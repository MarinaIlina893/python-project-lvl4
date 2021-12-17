from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    executor = models.ForeignKey(User, related_name='executor',
                                 on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, related_name='author',
                               on_delete=models.CASCADE, editable=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField('labels.Label',
                                    related_name='labels', blank=True)
    objects = models.Manager()
