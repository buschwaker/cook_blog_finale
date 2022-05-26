from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

from mptt.models import MPTTModel, TreeForeignKey


class MyUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        default='avatars/default-profile-image.png',
    )


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='children'
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        MyUser,
        related_name='posts',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/')
    slug = models.SlugField(max_length=200, default='some_slug')
    text = models.TextField()
    category = models.ForeignKey(
        Category, related_name='post', on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, related_name='post')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "post_single",
            kwargs={"slug": self.category.slug, "post_slug": self.slug}
        )

    class Meta:
        ordering = ['-id']


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    serves = models.CharField(max_length=50)
    prep_time = models.PositiveIntegerField(default=0)
    cook_time = models.PositiveIntegerField(default=0)
    ingredients = RichTextField()
    directions = RichTextField()
    post = models.ForeignKey(
        Post, related_name='recipe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Comment(models.Model):
    name = models.ForeignKey(
        MyUser,
        related_name='comments',
        on_delete=models.CASCADE
    )
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=dt.now())
    post = models.ForeignKey(
        Post, related_name='comment',
        on_delete=models.CASCADE,
    )
