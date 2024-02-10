from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime


class BlogPost(models.Model):
    owner = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content= models.CharField(max_length=140, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, default=timezone.now)
    readers = models.ManyToManyField(blank=True, null=True, related_name='readers', to=User)

    def __str__(self):
        return self.title