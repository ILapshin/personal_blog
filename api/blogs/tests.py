import json

from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from blogs.models import BlogPost


class SubscriptionsTests(APITestCase):
    def setUp(self):
        self.user_data = {'username':'Bob', 'password':'somerandompass'}
        self.user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])
        self.client.force_authenticate(self.user)

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