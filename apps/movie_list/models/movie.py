import uuid
from django.db import models


class Movie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    external_id = models.TextField(unique=True)
    title = models.TextField()
    # characters: ManyToManyField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
