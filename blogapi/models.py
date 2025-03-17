from django.db import models
from django.utils.text import slugify
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True, null=True)
    bio = models.TextField(_('bio'), blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    website = models.URLField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=15, blank=True, null=True)

    # Add these fields to resolve the clash
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_groups",  # Unique related_name
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Unique related_name
        related_query_name="customuser",
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

def get_anonymous_user():
    return CustomUser.objects.get_or_create(
        username='Anonymous',
        email='anonymous@example.com',
        defaults={'password': 'unusable'}
    )[0]

class Post(models.Model):
    class SectionChoices(models.TextChoices):
        TECHNOLOGY = "tech", "Technology"
        LIFESTYLE = "life", "Lifestyle"
        BUSINESS = "biz", "Business"

    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    section = models.CharField(
        max_length=10,
        choices=SectionChoices.choices,
        default=SectionChoices.TECHNOLOGY
    )
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name="blog_posts",
        default=get_anonymous_user
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)
    comments_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
