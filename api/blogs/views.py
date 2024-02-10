from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from blogs.models import BlogPost
from blogs.serializers import BlogPostSerializer

from subscriptions.models import Subscription


class BlogsPostView(APIView):
    def post(self, request: Request):
        data = {**request.data}
        data['owner'] = request.user.id
        serializer = BlogPostSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class BlogPostDeleteView(APIView):
    def delete(self, request: Request, post_id: int):
        blog_post = BlogPost.objects.filter(id=post_id)
        if not blog_post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostReadView(APIView):
    def post(self, request: Request, post_id: int):
        blog_post = get_object_or_404(BlogPost.objects, id=post_id)
        blog_post.readers.add(request.user)
        blog_post.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    
class BlogPostFeedView(APIView):
    def get(self, request: Request):
        subscriptions_query = Subscription.objects.filter(subscriber=request.user).values('owner')
        blog_posts_query = BlogPost.objects.filter(
            Q(owner__in=subscriptions_query)
        ).order_by(
            '-created_at'
        )[:500]

        serializer = BlogPostSerializer(blog_posts_query, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)