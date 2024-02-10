from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from django.contrib.auth.models import User
from subscriptions.models import Subscription


class SubscriptionsView(APIView):
    def post(self, request: Request, owner_id: int):
        owner = get_object_or_404(User.objects, pk=owner_id)
        new_subscription = Subscription(owner=owner, subscriber=request.user)
        new_subscription.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request: Request, owner_id: int):
        subscription = Subscription.objects.filter(owner=owner_id, subscriber=request.user)
        if not subscription:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)