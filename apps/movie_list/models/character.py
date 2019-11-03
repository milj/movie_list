import uuid
from django.db import models


class Character(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    external_id = models.TextField(unique=True)
    name = models.TextField()
    movies = models.ManyToManyField('Movie', related_name='characters')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
