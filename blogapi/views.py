from rest_framework import generics, permissions, authentication
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser




from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if not self.request.user or self.request.user.is_anonymous:
            raise ValueError("User must be authenticated to create a post.")
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require login to comment

    def perform_create(self, serializer):
        # Auto-set author to logged-in user
        serializer.save(user=self.request.user)

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"  # Enables lookup by slug instead of ID

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")  # ✅ Get the slug from URL
        print(f"Slug received: {slug}")  # ✅ Print slug to terminal
        return super().get(request, *args, **kwargs)

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
    
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])

def current_user(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
    })