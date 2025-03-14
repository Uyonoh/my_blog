from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
