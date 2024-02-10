from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from subscriptions.models import Subscription


class SubscriptionsTests(APITestCase):
    def setUp(self):
        self.user_data = [
            {'username':'Bob', 'password':'somerandompass'},   
            {'username':'Alice', 'password':'somerandompass'},        
        ]

        self.users = [
            User.objects.create_user(username=data['username'], password=data['password']) 
            for data in self.user_data
        ]

        self.client.force_authenticate(self.users[0])

    def test_subscriptions(self):
        initial_subscriptions = Subscription.objects.count()

        # subdcription creation
        resp = self.client.post('/api/v1/subscriptions/1')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(initial_subscriptions + 1, Subscription.objects.count())

        # subscription deletion
        resp = self.client.delete('/api/v1/subscriptions/1')        
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(initial_subscriptions, Subscription.objects.count())

