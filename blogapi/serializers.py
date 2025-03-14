from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "subtitle", "slug", "section", "thumbnail", "content", "author", "created_at", "updated_at", "total_likes", "comments_count"]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "text", "created_at"]