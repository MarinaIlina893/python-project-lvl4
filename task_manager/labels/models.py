from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField('tasks.Task')
    objects = models.Manager()

    def __str__(self):
        return self.name
