from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class BlogPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content= models.CharField(max_length=140, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, default=datetime.utcnow())
    readers = models.ManyToManyField(blank=True, related_name='readers', to=User)

    def __str__(self):
        return self.title