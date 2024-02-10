from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')