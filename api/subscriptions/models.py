from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')