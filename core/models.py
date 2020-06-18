from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.


class Content(models.Model):
    """Content to be created, displayed, updated, delete"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.title
