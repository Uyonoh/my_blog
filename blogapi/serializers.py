from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Show author as read-only
    total_likes = serializers.IntegerField(read_only=True)
    formatted_created_at = serializers.SerializerMethodField()
    formatted_updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        model = Post
        fields = ['id', 'title', 'subtitle', 'slug', 'section', 
                 'thumbnail', 'content', 'author', 'formatted_created_at',  'formatted_updated_at', 'total_likes',
                   ]
        read_only_fields = ['slug', 'author', 'created_at']
        extra_kwargs = {
            'thumbnail': {'required': False},
            'author': {'read_only': True}
        }

    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime('%b %d, %Y')

    def get_formatted_updated_at(self, obj):
        return obj.created_at.strftime('%b %d, %Y')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "text", "created_at"]