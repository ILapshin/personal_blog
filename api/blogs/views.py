from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from blogs.models import BlogPost
from blogs.serializers import BlogPostSerializer


class FeedView(APIView):

    def get(self, request: Request):
        return Response({'hello': 'world'})


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