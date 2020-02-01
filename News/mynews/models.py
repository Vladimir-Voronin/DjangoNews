from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class News(models.Model):
    SUBJECTS = (
        ('economics', 'Economics'),
        ('natural', 'Natural')
    )

    CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, unique_for_date='time_publish')
    body = models.TextField(max_length=5000, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    time_create = models.DateTimeField(auto_now_add=True)
    time_publish = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)
    subject_name = models.CharField(max_length=20, choices=SUBJECTS, default='economics')
    tags = models.ManyToManyField('Tag', related_name='news', blank=True)
    status = models.CharField(max_length=10, choices=CHOICES, default='draft')
    objects = models.Manager()
    published = NewsManager()

    class Meta:
        ordering = ['-time_publish']

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)


