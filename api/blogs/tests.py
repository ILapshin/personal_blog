import json

from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from blogs.models import BlogPost
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

    def _create_new_blog_post(self):
        data = {
            'title': 'Test Title',
            'content': 'Test post content.',
        }
         
        resp = self.client.post('/api/v1/blogs/posts', json.dumps(data), content_type='application/json')
        return resp

    def test_create_blog_post(self):
        initial_posts = BlogPost.objects.count()
        resp = self._create_new_blog_post()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual( BlogPost.objects.count(), initial_posts + 1)

    def test_delete_blog_post(self):
        new_post = self._create_new_blog_post()
        post_id = new_post.data['id']
        initial_posts = BlogPost.objects.count()

        resp = self.client.delete(f'/api/v1/blogs/posts/{post_id}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), initial_posts - 1)

    def test_read_blog_post(self):
        new_post = self._create_new_blog_post()
        post_id = new_post.data['id']

        resp = self.client.post(f'/api/v1/blogs/posts/{post_id}/read')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
    
    def test_feed(self):
        BlogPost.objects.all().delete()
        Subscription.objects.create(owner=self.users[0], subscriber=self.users[1])

        num_posts = 50
        for _ in range(num_posts):
            self._create_new_blog_post()
        
        self.client.force_authenticate(self.users[1])
        resp = self.client.get('/api/v1/blogs/feed')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), num_posts)
