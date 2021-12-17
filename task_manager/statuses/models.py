from django.db import models
# Create your models here.


class Status(models.Model):
    Name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.Name
