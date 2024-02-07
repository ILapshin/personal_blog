from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    pass