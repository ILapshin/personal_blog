from rest_framework.serializers import ModelSerializer, SerializerMethodField

from blogs.models import BlogPost
        

class BlogPostSerializer(ModelSerializer):

    is_read = SerializerMethodField(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'owner',
            'title',
            'content',
            'created_at',
            'is_read',
        )

    def get_is_read(self, blog_post):
        context = self.parent.context if self.parent else self.context
        user = context.get('request').user
        return user in blog_post.readers.all()