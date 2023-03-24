from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'DRAFT'), (1, 'POST'))


class Post(models.Model):
    """
    Class for site blog
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
        )
    created_on = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField()
    content = models.TextField()
    featured_image = CloudinaryField(
        'image',
        default='placeholder'
        )
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
