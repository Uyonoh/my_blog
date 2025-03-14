from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    formatted_created_at = serializers.SerializerMethodField()
    formatted_updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "subtitle", "slug", "section", "thumbnail", "content", "author", "formatted_created_at", "formatted_updated_at", "total_likes", "comments_count"]
    
    def get_formatted_created_at(self, obj):
        return obj.created_at.strftime('%b %d, %Y')
    
    def get_formatted_updated_at(self, obj):
        return obj.created_at.strftime('%b %d, %Y')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "text", "created_at"]