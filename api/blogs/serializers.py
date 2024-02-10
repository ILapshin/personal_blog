from rest_framework.serializers import ModelSerializer, SerializerMethodField

from blogs.models import BlogPost
        

class BlogPostSerializer(ModelSerializer):

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'owner',
            'title',
            'content',
            'created_at',
        )