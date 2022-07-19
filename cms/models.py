from django.db import models
import uuid
from account.models import User


class Post(models.Model):

    POST_TYPES = (
        ('NEWS', 'News'),
        ('EVENT', 'Event'),
    )
   
    title = models.CharField(max_length=500, unique=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')


    def __str__(self):
        return self.title



class Story(models.Model):
    title = models.CharField(max_length=500, unique=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Stories'


class Photo(models.Model):
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.description

class Video(models.Model):
    description = models.CharField(max_length=500)
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    

    def __str__(self):
        return self.description
