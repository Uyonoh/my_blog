from rest_framework import generics, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]  # Adjust as needed

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require login to comment

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"  # Enables lookup by slug instead of ID

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")  # ✅ Get the slug from URL
        print(f"Slug received: {slug}")  # ✅ Print slug to terminal
        return super().get(request, *args, **kwargs)


# # Post List & Create
# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.AllowAny]  # Publicly accessible

# # Post Detail, Update & Delete
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.AllowAny]  # Update this to IsAuthenticated if needed

# # Comment List & Create
# class CommentListCreateView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can comment

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# # Like/Unlike a Post
# @api_view(["POST"])
# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     user = request.user

#     if user in post.likes.all():
#         post.likes.remove(user)  # Unlike
#         message = "Post unliked"
#     else:
#         post.likes.add(user)  # Like
#         message = "Post liked"

#     post.save()
#     return Response({"message": message, "total_likes": post.total_likes()})
