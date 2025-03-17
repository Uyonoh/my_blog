from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PostListCreateView, PostDetailView, CommentListCreateView, like_post

# router = DefaultRouter()
# router.register(r'/posts', PostViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]



# urlpatterns = [
#     path("posts/", PostListCreateView.as_view(), name="post-list"),
#     path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
#     path("comments/", CommentListCreateView.as_view(), name="comment-list"),
#     path("posts/<int:post_id>/like/", like_post, name="like-post"),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from .views import PostViewSet, CommentViewSet, PostDetailView, SignupView, current_user
from django.conf import settings

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet)  # Generates /api/posts/
router.register(r'comments', CommentViewSet)  # Generates /api/comments/


urlpatterns = [
    path("", include(router.urls)),  # Include all router-generated URLs
    path("auth/login/", ObtainAuthToken.as_view(), name="api-login"),
    path("auth/signup/", SignupView.as_view(), name="api-signup"),
    path("auth/user/", current_user, name="current-user"),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]